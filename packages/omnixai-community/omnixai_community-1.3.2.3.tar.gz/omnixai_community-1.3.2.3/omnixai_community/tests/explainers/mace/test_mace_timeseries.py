#
# Copyright (c) 2023 salesforce.com, inc.
# All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
# For full license text, see the LICENSE file in the repo root or https://opensource.org/licenses/BSD-3-Clause
#
import os
import unittest
import numpy as np
import pandas as pd
from omnixai_community.utils.misc import set_random_seed
from omnixai_community.data.timeseries import Timeseries
from omnixai_community.explainers.timeseries.counterfactual.mace import MACEExplainer


def load_timeseries():
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../datasets")
    df = pd.read_csv(os.path.join(data_dir, "timeseries.csv"))
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit='s')
    df = df.rename(columns={"horizontal": "values"})
    df = df.set_index("timestamp")
    df = df.drop(columns=["anomaly"])
    return df


def train_detector(train_df):
    threshold = np.percentile(train_df["values"].values, 90)

    def _detector(ts: Timeseries):
        anomaly_scores = np.sum((ts.values > threshold).astype(int))
        return anomaly_scores / ts.shape[0]

    return _detector


class TestMACETimeseries(unittest.TestCase):

    def setUp(self) -> None:
        df = load_timeseries()
        self.train_df = df.iloc[:9150]
        self.test_df = df.iloc[9150:9300]
        self.detector = train_detector(self.train_df)
        print(self.detector(Timeseries.from_pd(self.test_df)))

    def test(self):
        set_random_seed()
        explainer = MACEExplainer(
            training_data=Timeseries.from_pd(self.train_df),
            predict_function=self.detector,
            threshold=0.001
        )
        explanations = explainer.explain(Timeseries.from_pd(self.test_df))
        fig = explanations.plotly_plot()


if __name__ == "__main__":
    unittest.main()
