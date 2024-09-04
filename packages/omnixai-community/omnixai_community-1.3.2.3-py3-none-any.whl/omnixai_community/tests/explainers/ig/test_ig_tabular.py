#
# Copyright (c) 2023 salesforce.com, inc.
# All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
# For full license text, see the LICENSE file in the repo root or https://opensource.org/licenses/BSD-3-Clause
#
import os
import pprint
import unittest
import torch
import torch.nn as nn
import tensorflow as tf
import numpy as np
import pandas as pd
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from omnixai_community.data.tabular import Tabular
from omnixai_community.explainers.tabular import IntegratedGradientTabular


class InputData(Dataset):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __len__(self):
        return self.x.shape[0]

    def __getitem__(self, index):
        return self.x[index], self.y[index]

    @staticmethod
    def collate_func(samples):
        x = torch.FloatTensor([sample[0] for sample in samples])
        y = torch.FloatTensor([sample[1] for sample in samples])
        return x, y


def init_weights(m):
    if isinstance(m, nn.Linear):
        torch.nn.init.xavier_uniform_(m.weight)
        m.bias.data.fill_(0.0)


class TestComputeIG(unittest.TestCase):
    @staticmethod
    def diabetes_data(file_path="diabetes.csv"):
        data = pd.read_csv(file_path)
        data = data.replace(
            to_replace=["Yes", "No", "Positive", "Negative", "Male", "Female"], value=[1, 0, 1, 0, 1, 0]
        )
        features = [
            "Age",
            "Gender",
            "Polyuria",
            "Polydipsia",
            "sudden weight loss",
            "weakness",
            "Polyphagia",
            "Genital thrush",
            "visual blurring",
            "Itching",
            "Irritability",
            "delayed healing",
            "partial paresis",
            "muscle stiffness",
            "Alopecia",
            "Obesity",
        ]

        y = data["class"]
        data = data.drop(["class"], axis=1)
        x_train_un, x_test_un, y_train, y_test = train_test_split(data, y, test_size=0.2, random_state=2, stratify=y)

        sc = StandardScaler()
        x_train = sc.fit_transform(x_train_un)
        x_test = sc.transform(x_test_un)

        x_train = x_train.astype(np.float32)
        y_train = y_train.to_numpy()
        x_test = x_test.astype(np.float32)
        y_test = y_test.to_numpy()

        return x_train, y_train, x_test, y_test, features, x_train_un, x_test_un

    @staticmethod
    def train_tf_model(x_train, y_train, x_test, y_test):
        model = tf.keras.models.Sequential()
        model.add(tf.keras.layers.Input(shape=(16,)))
        model.add(tf.keras.layers.Dense(units=128, activation=tf.keras.activations.softplus))
        model.add(tf.keras.layers.Dense(units=64, activation=tf.keras.activations.softplus))
        model.add(tf.keras.layers.Dense(units=1, activation=None))
        model.add(tf.keras.layers.Activation(tf.keras.activations.sigmoid))

        learning_rate = tf.keras.optimizers.schedules.ExponentialDecay(
            initial_learning_rate=0.1, decay_steps=1, decay_rate=0.99, staircase=True
        )
        optimizer = tf.keras.optimizers.SGD(learning_rate=learning_rate, momentum=0.9, nesterov=True)
        loss = tf.keras.losses.BinaryCrossentropy()
        metrics = [tf.keras.metrics.BinaryAccuracy(), tf.keras.metrics.AUC()]
        model.compile(optimizer=optimizer, loss=loss, metrics=metrics)
        model.fit(x_train, y_train, batch_size=242, epochs=200, verbose=0)
        train_loss, train_accuracy, train_auc = model.evaluate(x_train, y_train, batch_size=51, verbose=0)
        test_loss, test_accuracy, test_auc = model.evaluate(x_test, y_test, batch_size=51, verbose=0)

        print(
            "Train loss: {:.4f}\tTrain Accuracy: {:.4f}\tTrain AUC: {:.4f}".format(
                train_loss, train_accuracy, train_auc
            )
        )
        print("Test loss: {:.4f}\tTest Accuracy: {:.4f}\tTest AUC: {:.4f}".format(test_loss, test_accuracy, test_auc))

        y_pred = model.predict(x_test)
        y_pred_discrete = (y_pred > 0.5).astype(int)[:, 0]

        tpr = np.sum(y_test[y_test == 1] == y_pred_discrete[y_test == 1]) / np.sum(y_test == 1)
        tnr = np.sum(y_test[y_test == 0] == y_pred_discrete[y_test == 0]) / np.sum(y_test == 0)
        print("True Positive Rate: {:.4f}\t True Negative Rate: {:.4f}".format(tpr, tnr))
        return model

    @staticmethod
    def train_torch_model(x_train, y_train, x_test, y_test):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model = nn.Sequential(
            nn.Linear(x_train.shape[1], 128), nn.Softplus(), nn.Linear(128, 64), nn.Softplus(), nn.Linear(64, 1)
        ).apply(init_weights)
        model = model.to(device)

        learning_rate = 1e-3
        batch_size = 128
        num_epochs = 200
        optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
        loss_func = nn.BCEWithLogitsLoss()

        train_data = DataLoader(
            dataset=InputData(x_train, y_train), batch_size=batch_size, collate_fn=InputData.collate_func, shuffle=True
        )
        model.train()
        for epoch in range(num_epochs):
            total_loss = 0
            for i, (x, y) in enumerate(train_data):
                x, y = x.to(device), y.to(device).view((-1, 1))
                loss = loss_func(model(x), y)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
                total_loss += loss.data
            print("epoch: {}, training loss: {}".format(epoch, total_loss / len(train_data)))

        test_data = DataLoader(
            dataset=InputData(x_test, y_test), batch_size=32, collate_fn=InputData.collate_func, shuffle=False
        )
        probabilities = []
        for i, (x, y) in enumerate(test_data):
            x = x.to(device)
            prob = nn.Sigmoid()(model(x)).detach().cpu().numpy()
            probabilities.append(prob.reshape((-1,)))
        probabilities = np.concatenate(probabilities)
        predictions = np.array([int(p >= 0.5) for p in probabilities])

        tpr = np.sum(y_test[y_test == 1] == predictions[y_test == 1]) / np.sum(y_test == 1)
        tnr = np.sum(y_test[y_test == 0] == predictions[y_test == 0]) / np.sum(y_test == 0)
        print("True Positive Rate: {:.4f}\t True Negative Rate: {:.4f}".format(tpr, tnr))
        return model

    def test_tf(self):
        file_path = os.path.dirname(os.path.abspath(__file__)) + "/../../datasets/diabetes.csv"
        x_train, y_train, x_test, y_test, feature_names, x_train_un, x_test_un = self.diabetes_data(file_path)
        print("x_train shape: {}".format(x_train.shape))
        print("x_test shape: {}".format(x_test.shape))

        model = self.train_tf_model(x_train, y_train, x_test, y_test)
        tabular_data = Tabular(x_train, feature_columns=feature_names)
        explainer = IntegratedGradientTabular(
            training_data=tabular_data, model=model, preprocess_function=lambda x: x.to_numpy()
        )
        explanations = explainer.explain(x_test[:1])
        for e in explanations.get_explanations():
            print(e["instance"])
            print(f"Target label: {e['target_label']}")
            pprint.pprint(list(zip(e["features"], e["values"], e["scores"])))

        '''
        base_folder = os.path.dirname(os.path.abspath(__file__))
        directory = f"{base_folder}/../../datasets/tmp"
        explainer.save(directory=directory)
        explainer = IntegratedGradientTabular.load(directory=directory)
        explanations = explainer.explain(x_test[:1])
        for e in explanations.get_explanations():
            print(e["instance"])
            print(f"Target label: {e['target_label']}")
            pprint.pprint(list(zip(e["features"], e["values"], e["scores"])))
        '''

    def test_torch(self):
        file_path = os.path.dirname(os.path.abspath(__file__)) + "/../../datasets/diabetes.csv"
        x_train, y_train, x_test, y_test, feature_names, x_train_un, x_test_un = self.diabetes_data(file_path)
        print("x_train shape: {}".format(x_train.shape))
        print("x_test shape: {}".format(x_test.shape))

        model = self.train_torch_model(x_train, y_train, x_test, y_test)
        tabular_data = Tabular(x_train, feature_columns=feature_names)
        explainer = IntegratedGradientTabular(
            training_data=tabular_data, model=model, preprocess_function=lambda x: x.to_numpy()
        )
        explanations = explainer.explain(x_test[:1])
        for e in explanations.get_explanations():
            print(e["instance"])
            print(f"Target label: {e['target_label']}")
            pprint.pprint(list(zip(e["features"], e["values"], e["scores"])))


if __name__ == "__main__":
    unittest.main()
