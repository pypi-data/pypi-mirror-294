import random
import time
import torch
from dataclasses import dataclass

from src.imaaage.styles import apply_style, default_style_name
from src.imaaage.resolutions import resolutions, default_resolution
from src.imaaage.performance import perform_performance, default_performance
from src.imaaage.path import get_lora_path, default_base_model_name
from src.imaaage.adapters import set_lora, set_sampler


@dataclass
class Payload:
    prompt: str
    negative_prompt: str = ""
    image_seed: int = 0
    image_num: int = 1


@dataclass
class Preset:
    base_model_name: str = default_base_model_name
    refiner_model_name: str = 'None'
    vae_model_name: str = 'None'
    lora_model_names: list[tuple[str, float]] = None
    embedding_model_names: dict[str, str] = None
    lcm_lora: tuple[str, float] = None
    deep_cache: dict = None
    enable_prompt_weight: bool = False
    fuse_lora: bool = False

    resolution: str = default_resolution
    performance: str = default_performance
    prompt_style: str = default_style_name
    guidance_scale: float = 7.5
    clip_skip: int = 0
    switch: int = 24
    steps: int = 30
    sampler: str = "DPM++ 2M Karras"

    def collate(self):
        if self.lora_model_names is not None:
            self.lora_model_names = list(filter(
                lambda k: k[0] != "None" and k[1] > 0, self.lora_model_names))

        for k, v in perform_performance(self.performance).items():
            if hasattr(self, k):
                setattr(self, k, v)
        return self

    def key(self):
        return (self.base_model_name, self.refiner_model_name,
                self.vae_model_name, self.lora_model_names,
                self.embedding_model_names, self.lcm_lora,
                self.deep_cache, self.enable_prompt_weight)


class SDXLPipelineFactory:
    cached_key = None
    cached_value = (None, None)

    @classmethod
    def get_pipeline(cls, preset: Preset):
        if preset.key() == cls.cached_key:
            print("use cached pipeline")
            return cls.cached_value

        instance = cls.create_pipeline(preset)
        cls.cached_key = preset.key()
        cls.cached_value = instance
        return instance

    @classmethod
    def create_pipeline(cls, preset: Preset):
        from diffusers import StableDiffusionXLPipeline, StableDiffusionXLImg2ImgPipeline

        if preset.base_model_name.endswith("safetensors"):
            base_pipe = StableDiffusionXLPipeline.from_single_file(
                pretrained_model_link_or_path=preset.base_model_name,
                use_safetensors=True,
                torch_dtype=torch.float16)
        else:
            base_pipe = StableDiffusionXLPipeline.from_pretrained(
                pretrained_model_name_or_path=preset.base_model_name,
                torch_dtype=torch.float16,
                variant="fp16",
                feature_extractor=None,
                add_watermarker=False)
        base_pipe.to("cuda")

        refiner_pipe = None

        if preset.refiner_model_name is not None and preset.refiner_model_name != 'None':
            if preset.refiner_model_name.endswith("safetensors"):
                refiner_pipe = StableDiffusionXLImg2ImgPipeline.from_single_file(
                    pretrained_model_link_or_path=preset.refiner_model_name,
                    use_safetensors=True,
                    torch_dtype=torch.float16,
                    vae=base_pipe.vae)
                refiner_pipe.text_encoder_2 = base_pipe.text_encoder_2
            else:
                refiner_pipe = StableDiffusionXLImg2ImgPipeline.from_pretrained(
                    preset.refiner_model_name,
                    text_encoder_2=base_pipe.text_encoder_2,
                    vae=base_pipe.vae,
                    torch_dtype=torch.float16,
                    variant="fp16",
                    add_watermarker=False)
            refiner_pipe.to("cuda")

        lora_list: list[tuple[str, float]] = []
        if preset.lora_model_names is not None:
            lora_list = preset.lora_model_names.copy()
        if preset.lcm_lora is not None:
            lora_list.append(preset.lcm_lora)

        if len(lora_list) > 0:
            lora_list = [(get_lora_path(name), weight) for name, weight in lora_list]
            base_pipe = set_lora(base_pipe, lora_list, preset.fuse_lora)

        if preset.deep_cache is not None:
            from DeepCache import DeepCacheSDHelper

            helper = DeepCacheSDHelper(pipe=base_pipe)
            helper.set_params(**preset.deep_cache)
            helper.enable()
            print("set deep cache")

        return base_pipe, refiner_pipe

    @classmethod
    def clear(cls):
        cls.cached_key = None
        cls.cached_value = (None, None)


class SDXLPipeline:
    def __init__(self, preset: Preset, warm_up=False):
        self.preset = preset
        self.base, self.refiner = SDXLPipelineFactory.get_pipeline(preset)
        self.outputs = []

        if warm_up:
            self.warm_up()

    def warm_up(self):
        self.base("test", num_inference_steps=6)
        print(f"[WarmUp OK] cuda memory: {torch.cuda.memory_reserved() / 1024 / 1024} M")

    def run(self, payload: Payload, enable_preview=False):
        preset = self.preset

        prompt_style = self.preset.prompt_style
        prompt, neg_prompt = payload.prompt, payload.negative_prompt
        resolution = preset.resolution

        p_txt, n_txt = apply_style(prompt_style, prompt, neg_prompt)
        width, height = resolutions[resolution]
        max_seed = int(1024 * 1024 * 1024)
        seed = payload.image_seed
        if not isinstance(seed, int):
            seed = random.randint(1, max_seed)
        if seed < 0:
            seed = - seed
        seed = seed % max_seed
        steps = preset.steps
        image_num = payload.image_num
        switch = preset.switch
        guidance_scale = preset.guidance_scale
        clip_skip = preset.clip_skip

        preview_callback = None
        if enable_preview:
            from src.imaaage.callback import latents_preview
            def preview_callback(pipe, step, time_step, callback_kwargs):
                latents = callback_kwargs["latents"]
                image = latents_preview(latents)

                done_steps = i * steps + step
                progress = int(100.0 * float(done_steps) / float(steps * image_num))
                self.outputs.append([progress, f'采样进度{step}/{steps}', image])
                return callback_kwargs

        results = []
        logs = []
        for i in range(image_num):
            begin = time.time()

            switch_frac, base_output_type = None, "pil"
            if self.refiner is not None and switch < steps:
                switch_frac = switch / steps
                base_output_type = "latent"

            self.base = set_sampler(self.base, preset.sampler)
            images = self.base(
                prompt=p_txt,
                negative_prompt=n_txt,
                width=width,
                height=height,
                denoising_end=switch_frac,
                num_inference_steps=steps,
                guidance_scale=guidance_scale,
                generator=torch.Generator(device="cuda").manual_seed(seed),
                callback_on_step_end=preview_callback,
                output_type=base_output_type,
                clip_skip=clip_skip,
            ).images

            if switch_frac is not None:
                self.refiner = set_sampler(self.refiner, preset.sampler)
                images = self.refiner(
                    prompt=p_txt,
                    negative_prompt=n_txt,
                    image=images,
                    denoising_start=switch_frac,
                    num_inference_steps=steps,
                    guidance_scale=guidance_scale,
                    generator=torch.Generator(device="cuda").manual_seed(seed),
                    callback_on_step_end=preview_callback,
                    clip_skip=clip_skip,
                ).images

            consume = time.time() - begin

            torch.cuda.empty_cache()
            for x in images:
                d = [
                    ('Original Prompt', prompt),
                    ('Original Negative Prompt', neg_prompt),
                    ('Guidance Scale', guidance_scale),
                    ('Prompt', p_txt),
                    ('Negative Prompt', n_txt),
                    ('Switch', switch),
                    ('Clip Skip', clip_skip),
                    ('Style', prompt_style),
                    ('Performance', preset.performance),
                    ('Resolution', str((width, height))),
                    ('Base Model', preset.base_model_name),
                    ('Refiner Model', preset.refiner_model_name),
                    ('Seed', seed),
                    ('Consume', f'{consume:.2f}')
                ]
                if preset.lora_model_names is not None:
                    for n, w in preset.lora_model_names:
                        d.append((f'LoRA [{n}] weight', w))
                logs.append((x, d))
            results += images

        return results, logs
