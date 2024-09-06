from concurrent.futures import ThreadPoolExecutor

from imaaage.log import log_img
from imaaage.pipeline import Payload, SDXLPipeline, Preset


class Executor:
    outputs = []
    pool = ThreadPoolExecutor(max_workers=1)

    @classmethod
    def run(cls, preset: Preset, payload: Payload):
        pipe = SDXLPipeline(preset)
        cls.outputs = pipe.outputs

        res, histories = pipe.run(payload, enable_preview=True)
        for x, d in histories:
            log_img(x, d)

        return res

    @classmethod
    def submit(cls, *args):
        prompt, negative_prompt, prompt_style, performance, \
        resolution, image_number, image_seed, base_model_name, refiner_model_name, \
        sampler, guidance_scale, clip_skip, switch, steps, \
        l1, w1, l2, w2, l3, w3 = args

        preset = Preset(
            base_model_name=base_model_name,
            refiner_model_name=refiner_model_name,
            lora_model_names=[(l1, w1), (l2, w2), (l3, w3)],
            resolution=resolution,
            prompt_style=prompt_style,
            performance=performance
        ).collate()

        payload = Payload(
            prompt=prompt,
            negative_prompt=negative_prompt,
            image_num=image_number,
            image_seed=image_seed
        )

        return cls.pool.submit(cls.run, preset, payload)
