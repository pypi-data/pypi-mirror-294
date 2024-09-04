#
# Copyright (c) 2023 salesforce.com, inc.
# All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
# For full license text, see the LICENSE file in the repo root or https://opensource.org/licenses/BSD-3-Clause
#
import os
import unittest
import pprint
from omnixai_community.utils.misc import set_random_seed
from omnixai_community.explainers.tabular.agnostic.gpt import GPTExplainer
from omnixai_community.tests.explainers.tasks import TabularClassification


class TestGPTExplainer(unittest.TestCase):

    def test(self):
        base_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
        task = TabularClassification(base_folder).train_adult(num_training_samples=2000)
        predict_function = lambda z: task.model.predict_proba(task.transform.transform(z))

        set_random_seed()
        explainer = GPTExplainer(
            training_data=task.train_data,
            predict_function=predict_function,
            ignored_features=None,
            apikey="xxx"
        )

        i = 1653
        test_x = task.test_data.iloc(i)
        print(predict_function(test_x))
        explanations = explainer.explain(test_x)
        pprint.pprint(explanations.get_explanations(index=0)["text"])


if __name__ == "__main__":
    unittest.main()
