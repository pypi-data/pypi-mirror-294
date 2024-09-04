#
# Copyright (c) 2023 salesforce.com, inc.
# All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
# For full license text, see the LICENSE file in the repo root or https://opensource.org/licenses/BSD-3-Clause
#
import unittest
import pprint
from omnixai_community.utils.misc import set_random_seed
from omnixai_community.explainers.tabular.agnostic.ale import ALE
from omnixai_community.tests.explainers.tasks import TabularRegression
from omnixai_community.explanations.base import ExplanationBase


class TestALE(unittest.TestCase):

    def test(self):
        set_random_seed()
        task = TabularRegression().train_boston()
        predict_function = lambda z: task.model.predict(task.transform.transform(z))
        explainer = ALE(
            training_data=task.train_data, predict_function=predict_function, mode="regression"
        )
        explanations = explainer.explain()
        pprint.pprint(explanations.get_explanations())

        s = explanations.to_json()
        e = ExplanationBase.from_json(s)
        self.assertEqual(s, e.to_json())


if __name__ == "__main__":
    unittest.main()
