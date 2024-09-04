#
# Copyright (c) 2023 salesforce.com, inc.
# All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
# For full license text, see the LICENSE file in the repo root or https://opensource.org/licenses/BSD-3-Clause
#
import unittest
from omnixai_community.explainers.prediction import PredictionAnalyzer
from omnixai_community.tests.explainers.tasks import TabularRegression
from omnixai_community.explanations.base import ExplanationBase


class TestRegressionMetrics(unittest.TestCase):

    def test_regression_metric(self):
        task = TabularRegression().train_boston()
        predict_function = lambda z: task.model.predict(task.transform.transform(z))

        explainer = PredictionAnalyzer(
            predict_function=predict_function,
            test_data=task.test_data,
            test_targets=task.test_targets,
            mode="regression"
        )
        explanations = explainer._metric()
        print(explanations.get_explanations())
        explanations.plotly_plot()
        explanations.plot()

        s = explanations.to_json()
        e = ExplanationBase.from_json(s)
        self.assertEqual(s, e.to_json())
        e.plotly_plot()


if __name__ == "__main__":
    unittest.main()
