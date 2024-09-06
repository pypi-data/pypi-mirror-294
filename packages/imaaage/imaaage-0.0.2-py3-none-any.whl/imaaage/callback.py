import torch
from PIL import Image


# https://huggingface.co/blog/TimothyAlexisVass/explaining-the-sdxl-latent-space
def latents_preview(latents):
    """
    0: Luminance
    1: Cyan/Red => equivalent to rgb(0, 255, 255)/rgb(255, 0, 0)
    2: Lime/Medium Purple => equivalent to rgb(127, 255, 0)/rgb(127, 0, 255)
    3: Pattern/structure.
    """
    weights = (
        (60, -60, 25, -70),
        (60, -5, 15, -50),
        (60, 10, -5, -35)
    )

    weights_tensor = torch.t(torch.tensor(weights, dtype=latents.dtype).to(latents.device))  # [4, 3]
    biases_tensor = torch.tensor((150, 140, 130), dtype=latents.dtype).to(latents.device)
    rgb_tensor = torch.einsum("...lxy,lr -> ...rxy", latents, weights_tensor) + \
                 biases_tensor.unsqueeze(-1).unsqueeze(-1)
    image_array = rgb_tensor.clamp(0, 255)[0].byte().cpu().numpy()
    image_array = image_array.transpose(1, 2, 0)
    image = Image.fromarray(image_array)
    return image


