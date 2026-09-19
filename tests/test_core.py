import numpy as np
from sklearn.impute import KNNImputer
from sklearn.linear_model import LogisticRegression

from Network_Security.utils.main_utils.utils import evaluate_models
from Network_Security.utils.ml_utils.metric.classification_metric import (
    get_classification_score,
)
from Network_Security.utils.ml_utils.model.estimator import NetworkModel


def test_classification_metrics_are_finite_for_single_class_predictions():
    metrics = get_classification_score([0, 0], [0, 0])

    assert metrics.f1_score == 0
    assert metrics.precision_score == 0
    assert metrics.recall_score == 0


def test_network_model_transforms_before_predicting():
    features = np.array([[0.0], [1.0], [2.0], [3.0]])
    labels = np.array([0, 0, 1, 1])
    preprocessor = KNNImputer().fit(features)
    model = LogisticRegression().fit(preprocessor.transform(features), labels)

    prediction = NetworkModel(preprocessor, model).predict(np.array([[2.5]]))

    assert prediction.shape == (1,)


def test_model_evaluation_returns_f1_score():
    features = np.array([[0.0], [1.0], [2.0], [3.0], [4.0], [5.0]])
    labels = np.array([0, 0, 0, 1, 1, 1])
    report = evaluate_models(
        features,
        labels,
        features,
        labels,
        {"logistic": LogisticRegression()},
        {"logistic": {"C": [1.0]}},
    )

    assert 0 <= report["logistic"] <= 1
