import os
import gc
import torch


def set_lora(pipe, loras: list[tuple[str, float]], fuse=False):
    weights = []
    names = []

    for model_path, weight in loras:
        name = os.path.basename(model_path).split(".")[0]
        pipe.load_lora_weights(model_path, adapter_name=name)
        names.append(name)
        weights.append(weight)
        print(f">> load lora adapter: {name}, weight: {weight}")

    # pipe.fuse_lora()
    # torch.cuda.empty_cache()
    if len(names) > 0:
        pipe.set_adapters(adapter_names=names, adapter_weights=weights)
    print(f">> {torch.cuda.memory_reserved() / 1024 / 1024} M")
    return pipe


def set_vae(pipe, model_path: str, is_tiny=False):
    if is_tiny:
        from diffusers import AutoencoderTiny
        pipe.vae = AutoencoderTiny.from_pretrained(model_path).to(device=pipe.device, dtype=pipe.dtype)
        print(f">> load vae: {model_path}")
    else:
        from diffusers import AutoencoderKL
        pipe.vae = AutoencoderKL.from_pretrained(model_path).to(device=pipe.device, dtype=pipe.dtype)
        print(f">> load vae: {model_path}")
    return pipe


def set_embedding(pipe, params: dict[str, str]):
    paths, tokens = [], []

    for model_path, word in params:
        if not word:
            raise ValueError("embedding token is empty")
        paths.append(model_path)
        tokens.append(word)

    pipe.load_textual_inversion(pretrained_model_name_or_path=paths, token=tokens)
    print(f">> {torch.cuda.memory_reserved() / 1024 / 1024} M")
    return pipe


available_samplers = [
    "DPM++ 2M",
    "DPM++ 2M Karras",
    "DPM++ 2M SDE",
    "DPM++ 2M SDE Karras",
    "DPM++ 2S a",
    "DPM++ 2S a Karras",
    "DPM++ SDE",
    "DPM++ SDE Karras",
    "DPM2",
    "DPM2 Karras",
    "DPM2 a",
    "DPM2 a Karras",
    "Euler",
    "Euler a",
    "Heun",
    "LMS",
    "LMS Karras",
    "DDIM",
    "UniPC",
    "LCM"
]


def set_sampler(pipe, method):
    # see more https://huggingface.co/docs/diffusers/v0.20.0/en/api/schedulers/overview
    if method == "DPM++ 2M":
        from diffusers import DPMSolverMultistepScheduler
        pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
    elif method == "DPM++ 2M Karras":
        from diffusers import DPMSolverMultistepScheduler
        pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config, use_karras_sigmas=True)
    elif method == "DPM++ 2M SDE":
        from diffusers import DPMSolverMultistepScheduler
        pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config,
                                                                 algorithm_type="sde-dpmsolver++")
    elif method == "DPM++ 2M SDE Karras":
        from diffusers import DPMSolverMultistepScheduler
        pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config,
                                                                 algorithm_type="sde-dpmsolver++",
                                                                 use_karras_sigmas=True)
    elif method == "DPM++ 2S a":
        from diffusers import DPMSolverSinglestepScheduler
        pipe.scheduler = DPMSolverSinglestepScheduler.from_config(pipe.scheduler.config)
    elif method == "DPM++ 2S a Karras":
        from diffusers import DPMSolverSinglestepScheduler
        pipe.scheduler = DPMSolverSinglestepScheduler.from_config(pipe.scheduler.config, use_karras_sigmas=True)
    elif method == "DPM++ SDE":
        from diffusers import DPMSolverSinglestepScheduler
        pipe.scheduler = DPMSolverSinglestepScheduler.from_config(pipe.scheduler.config)
    elif method == "DPM++ SDE Karras":
        from diffusers import DPMSolverSinglestepScheduler
        pipe.scheduler = DPMSolverSinglestepScheduler.from_config(pipe.scheduler.config, use_karras_sigmas=True)
    elif method == "DPM2":
        from diffusers import KDPM2DiscreteScheduler
        pipe.scheduler = KDPM2DiscreteScheduler.from_config(pipe.scheduler.config)
    elif method == "DPM2 Karras":
        from diffusers import KDPM2DiscreteScheduler
        pipe.scheduler = KDPM2DiscreteScheduler.from_config(pipe.scheduler.config, use_karras_sigmas=True)
    elif method == "DPM2 a":
        from diffusers import KDPM2AncestralDiscreteScheduler
        pipe.scheduler = KDPM2AncestralDiscreteScheduler.from_config(pipe.scheduler.config)
    elif method == "DPM2 a Karras":
        from diffusers import KDPM2AncestralDiscreteScheduler
        pipe.scheduler = KDPM2AncestralDiscreteScheduler.from_config(pipe.scheduler.config, use_karras_sigmas=True)
    elif method == "Euler":
        from diffusers import EulerDiscreteScheduler
        pipe.scheduler = EulerDiscreteScheduler.from_config(pipe.scheduler.config)
    elif method == "Euler a":
        from diffusers import EulerAncestralDiscreteScheduler
        pipe.scheduler = EulerAncestralDiscreteScheduler.from_config(pipe.scheduler.config)
    elif method == "Heun":
        from diffusers import HeunDiscreteScheduler
        pipe.scheduler = HeunDiscreteScheduler.from_config(pipe.scheduler.config)
    elif method == "LMS":
        from diffusers import LMSDiscreteScheduler
        pipe.scheduler = LMSDiscreteScheduler.from_config(pipe.scheduler.config)
    elif method == "LMS Karras":
        from diffusers import LMSDiscreteScheduler
        pipe.scheduler = LMSDiscreteScheduler.from_config(pipe.scheduler.config, use_karras_sigmas=True)
    elif method == "DDIM":
        from diffusers import DDIMScheduler
        pipe.scheduler = DDIMScheduler.from_config(pipe.scheduler.config)
    elif method == "UniPC":
        from diffusers import UniPCMultistepScheduler
        pipe.scheduler = UniPCMultistepScheduler.from_config(pipe.scheduler.config)
    elif method == "LCM":
        from diffusers import LCMScheduler
        pipe.scheduler = LCMScheduler.from_config(pipe.scheduler.config)
    else:
        print(f">> unsupported {method}, use default scheduler")
    return pipe


def clear():
    torch.cuda.empty_cache()
    gc.collect()
    print(f">> {torch.cuda.memory_reserved() / 1024 / 1024} M")
