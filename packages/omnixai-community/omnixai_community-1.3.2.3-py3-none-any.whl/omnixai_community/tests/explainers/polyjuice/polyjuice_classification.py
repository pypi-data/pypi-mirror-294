#
# Copyright (c) 2023 salesforce.com, inc.
# All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
# For full license text, see the LICENSE file in the repo root or https://opensource.org/licenses/BSD-3-Clause
#
import unittest
import transformers
import numpy as np

from omnixai_community.data.text import Text
from omnixai_community.explainers.nlp.counterfactual.polyjuice import Polyjuice


class TestPolyjuice(unittest.TestCase):

    def setUp(self) -> None:
        self.model = transformers.pipeline(
            "sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english", return_all_scores=True
        )

        def _predict(x):
            scores = []
            predictions = self.model(x.values)
            for pred in predictions:
                score = [0.0, 0.0]
                for d in pred:
                    if d['label'] == 'NEGATIVE':
                        score[0] = d['score']
                    else:
                        score[1] = d['score']
                scores.append(score)
            return np.array(scores)

        self.idx2label = {"NEGATIVE": 0, "POSITIVE": 1}
        self.explainer = Polyjuice(predict_function=_predict)

    def test_explain(self):
        x = Text([
            "What a great movie!",
            "it was a fantastic performance!",
            "best film ever",
            "such a great show!",
            "it was a horrible movie",
            "i've never watched something as bad"
        ])
        explanations = self.explainer.explain(x)

        from omnixai_community.visualization.dashboard import Dashboard
        dashboard = Dashboard(
            instances=x,
            local_explanations={"polyjuice": explanations}
        )
        dashboard.show()


if __name__ == "__main__":
    unittest.main()
