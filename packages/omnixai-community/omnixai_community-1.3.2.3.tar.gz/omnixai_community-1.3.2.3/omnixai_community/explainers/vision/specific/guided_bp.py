#
# Copyright (c) 2023 salesforce.com, inc.
# All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
# For full license text, see the LICENSE file in the repo root or https://opensource.org/licenses/BSD-3-Clause
#
from typing import Callable
from omnixai_community.utils.misc import is_tf_available, is_torch_available
from omnixai_community.explainers.base import ExplainerBase
from omnixai_community.data.image import Image
from omnixai_community.explanations.image.pixel_importance import PixelImportance
from .utils import GradMixin, guided_bp


class GuidedBP(ExplainerBase, GradMixin):
    """
    The guided back propagation method for vision models.
    """

    explanation_type = "local"
    alias = ["guidedbp", "guided-bp"]

    def __init__(
            self,
            model,
            preprocess_function: Callable,
            mode: str = "classification",
            **kwargs
    ):
        """
        :param model: The model to explain, whose type can be `tf.keras.Model` or `torch.nn.Module`.
        :param preprocess_function: The preprocessing function that converts the raw data
            into the inputs of ``model``.
        :param mode: The task type, e.g., `classification` or `regression`.
        """
        super().__init__()
        if not is_tf_available() and not is_torch_available():
            raise EnvironmentError("Both Torch and Tensorflow cannot be found.")

        self.model = model
        self.preprocess_function = preprocess_function
        self.mode = mode

    def explain(self, X: Image, y=None, **kwargs):
        """
        Generates the explanations for the input instances.

        :param X: A batch of input instances.
        :param y: A batch of labels to explain. For regression, ``y`` is ignored.
            For classification, the top predicted label of each input instance will be explained
            when `y = None`.
        :param kwargs: Additional parameters.
        :return: The explanations for all the instances, e.g., pixel importance scores.
        :rtype: PixelImportance
        """
        explanations = PixelImportance(self.mode)

        gradients, y = guided_bp(
            X=X,
            y=y,
            model=self.model,
            preprocess_function=self.preprocess_function,
            mode=self.mode,
            num_samples=1,
            sigma=0.0
        )
        for i in range(len(X)):
            label = y[i] if y is not None else None
            explanations.add(
                image=self._resize(self.preprocess_function, X[i]).to_numpy()[0],
                target_label=label,
                importance_scores=gradients[i]
            )
        return explanations
