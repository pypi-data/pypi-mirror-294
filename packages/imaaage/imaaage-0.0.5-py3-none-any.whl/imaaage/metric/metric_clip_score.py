import torch
import dataclasses
import numpy as np
from PIL import Image
from transformers import CLIPProcessor, CLIPModel

device = "cpu" if not torch.cuda.is_available() else "cuda"

CLIP_MAPPING = {
    "ViT-B/16": "openai/clip-vit-base-patch16",
    "ViT-B/32": "openai/clip-vit-base-patch32",
    "ViT-L/14": "openai/clip-vit-large-patch14",
}


@dataclasses.dataclass
class ClipScoreMetric:
    similarity: np.array


class ClipScoreEvaluator:
    def __init__(self, model_id: str = "ViT-B/32", device=device):
        model_id = CLIP_MAPPING[model_id]
        self.model = CLIPModel.from_pretrained(model_id).to(device)
        self.processor = CLIPProcessor.from_pretrained(model_id)
        print("ClipScoreEvaluator load ok")

    def evaluate(
            self,
            image: Image.Image | list[Image.Image],
            text: str | list[str]
    ):
        inputs = self.processor(text=text, images=image, return_tensors="pt", padding=True)
        inputs = {k: v.to(device) for k, v in inputs.items()}
        with torch.no_grad():
            outputs = self.model(**inputs)
        logits_per_image = outputs.logits_per_image
        sim = logits_per_image.cpu().detach().numpy()
        return ClipScoreMetric(similarity=sim)


if __name__ == '__main__':
    text = ["The blonde man", "The black hair girl"]
    img = [
        Image.open("/Users/yinyajun/Desktop/assets/aaaa.jpg"),
        Image.open("/Users/yinyajun/Desktop/assets/aaa.jpg")
    ]

    evaluator = ClipScoreEvaluator()
    res = evaluator.evaluate(img[0], text[0])
    print(res)
