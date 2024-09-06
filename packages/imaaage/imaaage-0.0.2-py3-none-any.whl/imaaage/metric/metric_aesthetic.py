import torch
import torch.nn as nn
import dataclasses
import numpy as np
from PIL import Image
from torch.hub import load_state_dict_from_url
from transformers import CLIPProcessor, CLIPModel

AESTHETIC_URL = "https://raw.githubusercontent.com/christophschuhmann/improved-aesthetic-predictor/main/sac%2Blogos%2Bava1-l14-linearMSE.pth"
device = "cuda" if torch.cuda.is_available() else "cpu"

CLIP_MAPPING = {
    "ViT-B/16": "openai/clip-vit-base-patch16",
    "ViT-B/32": "openai/clip-vit-base-patch32",
    "ViT-L/14": "openai/clip-vit-large-patch14",
}


class MLP(nn.Module):
    def __init__(self, input_size=768):
        super().__init__()
        self.input_size = input_size
        self.layers = nn.Sequential(
            nn.Linear(self.input_size, 1024),
            nn.Dropout(0.2),
            nn.Linear(1024, 128),
            nn.Dropout(0.2),
            nn.Linear(128, 64),
            nn.Dropout(0.1),
            nn.Linear(64, 16),
            nn.Linear(16, 1)
        )

    def forward(self, x):
        return self.layers(x)


@dataclasses.dataclass
class AestheticMetric:
    score: np.array


class AestheticEvaluator:
    def __init__(self, clip_model: str = "ViT-L/14", input_size=768, device=device):
        model_id = CLIP_MAPPING[clip_model]
        self.clip_model = CLIPModel.from_pretrained(model_id).to(device)
        self.processor = CLIPProcessor.from_pretrained(model_id)

        self.score_model = MLP(input_size)
        state_dict = load_state_dict_from_url(AESTHETIC_URL, progress=True, map_location="cpu")
        self.score_model.load_state_dict(state_dict)
        self.score_model = self.score_model.to(device).eval()
        print("AestheticEvaluator load ok")

    def evaluate(self, image: Image.Image | list[Image.Image]):
        inputs = self.processor(images=image, return_tensors="pt")
        inputs = {k: v.to(device) for k, v in inputs.items()}

        with torch.no_grad():
            image_features = self.clip_model.get_image_features(**inputs)
            image_embeds = image_features / image_features.norm(p=2, dim=-1, keepdim=True)
            score = self.score_model(image_embeds)
        score = score.cpu().detach().numpy().flatten()
        return AestheticMetric(score=score)


if __name__ == '__main__':
    img = Image.open("/Users/yinyajun/Desktop/assets/aaaa.jpg")

    # img = [
    #     Image.open("/Users/yinyajun/Desktop/assets/aaaa.jpg"),
    #     Image.open("/Users/yinyajun/Desktop/assets/aaa.jpg")
    # ]

    evaluator = AestheticEvaluator()
    res = evaluator.evaluate(img)
    print(res)
