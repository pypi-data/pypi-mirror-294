import os
from pathlib import Path
from urllib.parse import urlparse

imaaage_dir = os.path.join(Path.home(), ".cache/imaaage")
os.makedirs(imaaage_dir, exist_ok=True)

default_base_model_name = "RunDiffusion/Juggernaut-XL-v9"
default_refiner_model_name = "stabilityai/stable-diffusion-xl-refiner-1.0"
default_lora_name = 'sdxl_noise_off'
default_lora_weight = 0.5
default_lcm_lora = "lcm_lora_sdxl"

models = {
    default_base_model_name: default_base_model_name
}

refiners = {
    default_refiner_model_name: default_refiner_model_name
}

loras = {
    default_lora_name: 'https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/sd_xl_offset_example-lora_1.0.safetensors'
}

lcm = {
    default_lcm_lora: 'https://huggingface.co/latent-consistency/lcm-lora-sdxl/resolve/main/pytorch_lora_weights.safetensors'
}


def load_file_from_url(
        url: str,
        *,
        model_dir: str = imaaage_dir,
        progress: bool = True,
        file_name: str | None = None) -> str:
    os.makedirs(model_dir, exist_ok=True)
    if not file_name:
        parts = urlparse(url)
        file_name = os.path.basename(parts.path)
    cached_file = os.path.abspath(os.path.join(model_dir, file_name))
    if not os.path.exists(cached_file):
        print(f'Downloading: "{url}" to {cached_file}\n')
        from torch.hub import download_url_to_file
        download_url_to_file(url, cached_file, progress=progress)
    return cached_file


def download():
    from diffusers import StableDiffusionXLPipeline
    lora_dir = os.path.join(imaaage_dir, "lora")
    os.makedirs(lora_dir, exist_ok=True)

    for v in models.values():
        path = StableDiffusionXLPipeline.download(pretrained_model_name=v, variant="fp16")
        print(path)
    for v in refiners.values():
        path = StableDiffusionXLPipeline.download(pretrained_model_name=v, variant="fp16")
        print(path)
    for k, v in loras.items():
        path = load_file_from_url(v, model_dir=lora_dir, file_name=f"{k}.safetensors")
        print(path)
    for k, v in lcm.items():
        path = load_file_from_url(v, model_dir=lora_dir, file_name=f"{k}.safetensors")
        print(path)


def get_lora_path(name):
    lora_dir = os.path.join(imaaage_dir, "lora")
    file_name = os.path.join(lora_dir, f"{name}.safetensors")
    if not os.path.exists(file_name):
        raise FileNotFoundError(file_name)
    return file_name


if __name__ == '__main__':
    download()
