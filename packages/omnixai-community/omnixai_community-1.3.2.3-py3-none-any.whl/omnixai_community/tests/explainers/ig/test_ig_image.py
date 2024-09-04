#
# Copyright (c) 2023 salesforce.com, inc.
# All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
# For full license text, see the LICENSE file in the repo root or https://opensource.org/licenses/BSD-3-Clause
#
import os
import json
import unittest
import torch
from torchvision import models, transforms
from PIL import Image as PilImage

from omnixai_community.data.image import Image
from omnixai_community.explainers.vision import IntegratedGradientImage


class TestImageClassification(unittest.TestCase):
    def setUp(self) -> None:
        directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../datasets")
        self.img = Image(PilImage.open(os.path.join(directory, "images/boat.jpg")).convert("RGB"))
        self.model = models.inception_v3(pretrained=True)
        self.transform = transforms.Compose(
            [
                transforms.Resize((256, 256)),
                transforms.CenterCrop(224),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
            ]
        )
        self.preprocess = lambda ims: torch.stack([self.transform(im.to_pil()) for im in ims])

        with open(os.path.join(directory, "images/imagenet_class_index.json"), "r") as read_file:
            class_idx = json.load(read_file)
            self.idx2label = [class_idx[str(k)][1] for k in range(len(class_idx))]

    def test_explain(self):
        explainer = IntegratedGradientImage(model=self.model, preprocess_function=self.preprocess)
        explanations = explainer.explain(self.img)
        explanations.plot(class_names=self.idx2label)


if __name__ == "__main__":
    unittest.main()
