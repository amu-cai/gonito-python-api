from pydantic import BaseModel
from typing import Any

from metrics.metric_base import MetricBase
from metrics.accuracy import Accuracy
from metrics.mse import MSE
from metrics.rmse import RMSE
from metrics.fbeta import FBeta
from metrics.recall import Recall
from metrics.precision import Precision
from metrics.average_precision import AveragePrecision
from metrics.balanced_accuracy import BalancedAccuracy
from metrics.brier import Brier
from metrics.cohen_kappa import CohenKappa
from metrics.dcg import DCG
from metrics.hamming_loss import HammingLoss
from metrics.hinge_loss import HingeLoss
from metrics.log_loss import LogLoss
from metrics.matthews_correlation import MatthewsCorrelation
from metrics.ndcg import NDCG

class Metrics(BaseModel):
    """All available metrics."""

    accuracy: MetricBase = Accuracy
    balanced_accuracy: MetricBase = BalancedAccuracy
    fbeta_score: MetricBase = FBeta
    rmse: MetricBase = RMSE
    mse: MetricBase = MSE
    recall: MetricBase = Recall
    precision: MetricBase = Precision
    average_precision: MetricBase = AveragePrecision
    brier: MetricBase = Brier
    cohen_kappa: MetricBase = CohenKappa
    dcg: MetricBase = DCG
    hamming_loss: MetricBase = HammingLoss
    hinge_loss: MetricBase = HingeLoss
    log_loss: MetricBase = LogLoss
    matthews_correlation: MetricBase = MatthewsCorrelation
    ndcg: MetricBase = NDCG


def all_metrics() -> list[str]:
    """Show all available metrics."""
    return Metrics.model_fields.keys()


def metric_info(metric_name: str) -> dict:
    """Get information about a metric."""
    if metric_name not in all_metrics():
        print(f"Metric {metric_name} is not defined")
    else:
        metric = getattr(Metrics(), metric_name)
        return metric().info()


def calculate_default_metric(
    metric_name: str,
    expected: list[Any],
    out: list[Any],
) -> Any:
    """Use given metric with default settings."""
    if metric_name not in all_metrics():
        print(f"Metric {metric_name} is not defined")
    else:
        metric = getattr(Metrics(), metric_name)
        return metric().calculate(expected, out)


def calculate_metric(
    metric_name: str,
    expected: list[Any],
    out: list[Any],
    params: dict,
) -> Any:
    """Use given metric with non-default settings."""
    if metric_name not in all_metrics():
        print(f"Metric {metric_name} is not defined")
    else:
        metric = getattr(Metrics(), metric_name)
        metric_params = metric.model_fields.keys()

        if params == metric_params:
            return metric(**params).calculate(expected, out)
        else:
            print(f"Metric {metric_name} has the following params: {metric_params} and you gave those: {params}")
