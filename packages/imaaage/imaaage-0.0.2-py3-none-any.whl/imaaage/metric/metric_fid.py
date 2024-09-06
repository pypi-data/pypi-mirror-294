import os
import torch
import torch.nn.functional as F
import dataclasses
import numpy as np
from torchvision import transforms
from PIL import Image
from tqdm import tqdm
from typing import Literal

from .modules.inception import InceptionV3

device = "cpu" if not torch.cuda.is_available() else "cuda"


@dataclasses.dataclass
class FIDMetric:
    dist: float


class FIDEvaluator:
    def __init__(self, dims: Literal[64, 192, 768, 2048] = 2048, device=device):
        """
        64: 0,  # First max pooling features
        192: 1,  # Second max pooling features
        768: 2,  # Pre-aux classifier features
        2048: 3,  # Final average pooling features
        """
        self.dims = dims
        self.device = device
        self.model = InceptionV3([InceptionV3.BLOCK_INDEX_BY_DIM[dims]]).to(device)
        self.model = self.model.eval()
        self.transform = transforms.ToTensor()

    def calculate_dist(self, images: list[Image.Image], batch_size: int = 1, saved_npz: str = None):
        if batch_size > len(images):
            batch_size = len(images)

        preds = np.empty((len(images), self.dims))
        for idx in tqdm(range(0, len(images), batch_size)):
            batch = images[idx: idx + batch_size]
            batch = torch.stack([self.transform(i) for i in batch], )

            with torch.no_grad():
                pred = self.model(batch)[0]

            # If model output is not scalar, apply global spatial average pooling.
            # This happens if you choose a dimensionality not equal 2048.
            if pred.size(2) != 1 or pred.size(3) != 1:
                pred = F.adaptive_avg_pool2d(pred, output_size=(1, 1))

            pred = pred.squeeze(3).squeeze(2).cpu().numpy()
            preds[idx: idx + pred.shape[0]] = pred

        mu = np.mean(preds, axis=0)
        sigma = np.cov(preds, rowvar=False)  # 注意谁是变量
        if saved_npz is not None:
            np.savez_compressed(saved_npz, mu=mu, sigma=sigma)
        return mu, sigma

    def calculate_fid(self, mu1, sigma1, mu2, sigma2):
        """Numpy implementation of the Frechet Distance.
          The Frechet distance between two multivariate Gaussian X_1 ~ N(mu_1, C_1) and X_2 ~ N(mu_2, C_2) is
          d^2 = ||mu_1 - mu_2||^2 + Tr(C_1 + C_2 - 2*sqrt(C_1*C_2)).
        """
        mu1 = np.atleast_1d(mu1)
        mu2 = np.atleast_1d(mu2)
        sigma1 = np.atleast_2d(sigma1)
        sigma2 = np.atleast_2d(sigma2)

        assert mu1.shape == mu2.shape, "mean vectors should be same shape"
        assert sigma1.shape == sigma2.shape, "covariance matrices should be same shape"

        # 用linalg.sqrtm比较容易出现数值不稳定，sum(eigvals) == trace
        diff = mu1 - mu2
        tr_cov_mean = np.sum(np.sqrt(np.linalg.eigvals(sigma1.dot(sigma2)).astype("complex128")).real)
        return float(diff.dot(diff) + np.trace(sigma1) + np.trace(sigma2) - 2 * tr_cov_mean)

    def evaluate(self,
                 images1: list[Image.Image],
                 images2: list[Image.Image] = None,
                 batch_size=1,
                 cached_npz1: str = None,
                 cached_npz2: str = None,
                 ):
        if images2 is None and cached_npz2 is None:
            raise ValueError("both images2 and cached_npz2 are None.")

        if cached_npz1 is None:
            mu1, sigma1 = self.calculate_dist(images1, batch_size)
        else:
            with np.load(cached_npz1) as f:
                mu1, sigma1 = f["mu"][:], f["sigma"][:]

        if cached_npz2 is None:
            mu2, sigma2 = self.calculate_dist(images2, batch_size)
        else:
            with np.load(cached_npz2) as f:
                mu2, sigma2 = f["mu"][:], f["sigma"][:]

        return FIDMetric(dist=self.calculate_fid(mu1, sigma1, mu2, sigma2))


if __name__ == '__main__':
    dir1 = "/Users/yinyajun/Desktop/assets/100_koreanBoy"
    dir2 = "/Users/yinyajun/Desktop/assets/100_koreanSmall"

    images1 = [Image.open(dir1 + "/" + i).convert("RGB") for i in os.listdir(dir1) if
               i.endswith(".png") or i.endswith("jpg")]
    images2 = [Image.open(dir2 + "/" + i).convert("RGB") for i in os.listdir(dir2) if
               i.endswith(".png") or i.endswith("jpg")]

    evaluator = FIDEvaluator()
    res = evaluator.evaluate(images1, images2, batch_size=1)
    print(res)
