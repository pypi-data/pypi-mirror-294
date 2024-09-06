import os
import pathlib
import dataclasses
import shutil

from PIL import Image

from .metric_fid import FIDEvaluator
from .metric_aesthetic import AestheticEvaluator
from .metric_clip_score import ClipScoreEvaluator


@dataclasses.dataclass
class SingleEvaluateResult:
    aesthetic_score: float
    clip_score: float = -1


@dataclasses.dataclass
class BatchEvaluateResult:
    fid: float


IMAGE_EXTENSIONS = {"bmp", "jpg", "jpeg", "pgm", "png", "ppm", "tif", "tiff", "webp"}


class ImageEvaluator:
    def __init__(self):
        self.fid = FIDEvaluator()
        self.clip_score = ClipScoreEvaluator()
        self.aesthetic = AestheticEvaluator()

    def evaluate_single(self, image: Image.Image, text: str = None):
        res = SingleEvaluateResult(aesthetic_score=self.aesthetic.evaluate(image).score[0])
        if text is not None:
            clip_res = self.clip_score.evaluate(image, text).similarity[0][0]
            res.clip_score = clip_res
        return res

    def evaluate_batch(self, images: list[Image.Image], reference_dir: str, batch_size: int = 1, force: bool = False):
        cached_npz = os.path.join(reference_dir, "cached_fid.npz")

        if force and os.path.exists(cached_npz):
            os.remove(cached_npz)

        if not os.path.exists(cached_npz):
            path = pathlib.Path(reference_dir)
            files = sorted([file for ext in IMAGE_EXTENSIONS for file in path.glob("*.{}".format(ext))])
            images2 = [Image.open(i).convert("RGB") for i in files]
            self.fid.calculate_dist(images2, batch_size, cached_npz)

        fid = self.fid.evaluate(images, batch_size=batch_size, cached_npz2=cached_npz)
        return BatchEvaluateResult(fid=fid.dist)


if __name__ == '__main__':
    evaluator = ImageEvaluator()

    text = "The blonde woman"
    img = Image.open("/Users/yinyajun/Desktop/assets/aaaa.jpg").convert("RGB")

    res = evaluator.evaluate_single(img, text)
    print(res)
