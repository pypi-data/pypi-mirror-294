from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from modelscope.outputs import OutputKeys

img = 'https://modelscope.oss-cn-beijing.aliyuncs.com/test/images/mog_face_detection.jpg'
image_quality_assessment_pipeline = pipeline(Tasks.image_quality_assessment_mos, 'damo/cv_man_image-quality-assessment')
result = image_quality_assessment_pipeline(img)[OutputKeys.SCORE]
print(result)

import sys
sys.exit(-1)



# ---
from torchvision import transforms

from PIL import Image
img = Image.open("/Users/yinyajun/Desktop/a.jpg")

transform_input = transforms.Compose([
    transforms.Resize(224),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5]),
])


input = transform_input(img).unsqueeze(0)
print(input.shape)





import torch
from copy import deepcopy
import json

""" configuration json """


class Config(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__

    @classmethod
    def load(cls, file):
        with open(file, 'r') as f:
            config = json.loads(f.read())
            return Config(config)


config = Config({
    # image path
    "image_path": "./test_images/kunkun.png",

    # valid times
    "num_crops": 20,

    # model
    "patch_size": 8,
    "img_size": 224,
    "embed_dim": 768,
    "dim_mlp": 768,
    "num_heads": [4, 4],
    "window_size": 4,
    "depths": [2, 2],
    "num_outputs": 1,
    "num_tab": 2,
    "scale": 0.8,

    # checkpoint path
    "ckpt_path": "/Users/yinyajun/.cache/modelscope/hub/damo/cv_man_image-quality-assessment/pytorch_model.pt",
})

# from modelscope.models.cv.image_quality_assessment_man.maniqa import MANIQA
from modules.maniqa import MANIQA

model = MANIQA(embed_dim=config.embed_dim, num_outputs=config.num_outputs, dim_mlp=config.dim_mlp,
             patch_size=config.patch_size, img_size=config.img_size, window_size=config.window_size,
             depths=config.depths, num_heads=config.num_heads, num_tab=config.num_tab, scale=config.scale)

load_net = torch.load(config.ckpt_path, map_location="cpu")["params"]
# remove unnecessary 'module.'
for k, v in deepcopy(load_net).items():
    if k.startswith('module.'):
        load_net[k[7:]] = v
        load_net.pop(k)


model.load_state_dict(load_net, strict=True)
model.eval()

res = model(input)
print(res)
