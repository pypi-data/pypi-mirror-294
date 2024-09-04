#
# Copyright (c) 2023 salesforce.com, inc.
# All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
# For full license text, see the LICENSE file in the repo root or https://opensource.org/licenses/BSD-3-Clause
#
import os
import unittest
from PIL import Image as PilImage
from omnixai_community.data.text import Text
from omnixai_community.data.image import Image
from omnixai_community.data.multi_inputs import MultiInputs


class TestMultiInputs(unittest.TestCase):

    def setUp(self) -> None:
        directory = os.path.dirname(os.path.abspath(__file__))
        img = Image(PilImage.open(os.path.join(directory, "../datasets/images/dog.jpg")))
        text = Text("A dog.")
        self.inputs = MultiInputs(image=img, text=text)

    def test(self):
        self.assertEqual(self.inputs.num_samples(), 1)
        print(self.inputs.image)
        print(self.inputs.text)
        print(self.inputs[0].image)
        print(self.inputs[0].text)


if __name__ == "__main__":
    unittest.main()
