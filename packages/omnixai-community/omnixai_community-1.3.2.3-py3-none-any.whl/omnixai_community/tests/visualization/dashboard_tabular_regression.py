#
# Copyright (c) 2023 salesforce.com, inc.
# All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
# For full license text, see the LICENSE file in the repo root or https://opensource.org/licenses/BSD-3-Clause
#
import unittest
import numpy as np
import pandas as pd
import sklearn
import sklearn.ensemble
from sklearn.datasets import fetch_california_housing

from omnixai_community.data.tabular import Tabular
from omnixai_community.preprocessing.base import Identity
from omnixai_community.preprocessing.tabular import TabularTransform
from omnixai_community.explainers.data import DataAnalyzer
from omnixai_community.explainers.tabular import TabularExplainer
from omnixai_community.explainers.prediction import PredictionAnalyzer
from omnixai_community.visualization.dashboard import Dashboard


class TestDashboard(unittest.TestCase):

    def setUp(self) -> None:
        housing = fetch_california_housing()
        df = pd.DataFrame(
            np.concatenate([housing.data, housing.target.reshape((-1, 1))], axis=1),
            columns=list(housing.feature_names) + ['target']
        )
        tabular_data = Tabular(df, target_column='target')

        transformer = TabularTransform(
            target_transform=Identity()
        ).fit(tabular_data)
        x = transformer.transform(tabular_data)

        x_train, x_test, y_train, y_test = \
            sklearn.model_selection.train_test_split(x[:, :-1], x[:, -1], train_size=0.80)
        print('Training data shape: {}'.format(x_train.shape))
        print('Test data shape:     {}'.format(x_test.shape))

        rf = sklearn.ensemble.RandomForestRegressor(n_estimators=200)
        rf.fit(x_train, y_train)
        print('MSError when predicting the mean', np.mean((y_train.mean() - y_test) ** 2))
        print('Random Forest MSError', np.mean((rf.predict(x_test) - y_test) ** 2))

        self.model = rf
        self.tabular_data = tabular_data
        self.features = list(df.columns)
        self.transformer = transformer
        self.preprocess = lambda z: transformer.transform(z)
        self.x_test = x_test
        self.test_data = transformer.invert(x_test)
        self.test_targets = y_test

    def test(self):
        explainer = DataAnalyzer(
            explainers=["correlation", "mutual", "chi2"],
            mode="regression",
            data=self.tabular_data
        )
        data_explanations = explainer.explain()

        explainer = PredictionAnalyzer(
            mode="regression",
            test_data=self.test_data,
            test_targets=self.test_targets,
            model=self.model,
            preprocess=self.preprocess
        )
        prediction_explanations = explainer.explain()

        explainers = TabularExplainer(
            explainers=["lime", "shap", "sensitivity", "pdp", "ale"],
            mode="regression",
            data=self.tabular_data,
            model=self.model,
            preprocess=self.preprocess,
            params={
                "lime": {"kernel_width": 3},
                "shap": {"nsamples": 100}
            }
        )
        # Apply an inverse transform, i.e., converting the numpy array back to `Tabular`
        test_instances = self.transformer.invert(self.x_test[0:5])
        # Generate explanations
        local_explanations = explainers.explain(X=test_instances)
        global_explanations = explainers.explain_global(
            params={"pdp": {"features": self.features[:6]}})

        dashboard = Dashboard(
            instances=test_instances,
            local_explanations=local_explanations,
            global_explanations=global_explanations,
            data_explanations=data_explanations,
            prediction_explanations=prediction_explanations
        )
        dashboard.show()


if __name__ == "__main__":
    unittest.main()
