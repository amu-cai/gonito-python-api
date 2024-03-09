from pydantic import BaseModel
from typing import Any

from metric_base import MetricBase
from accuracy import Accuracy
from mse import MSE
from rmse import RMSE
from fbeta import FBeta
from recall import Recall
from precision import Precision
from average_precision import AveragePrecision
from balanced_accuracy import BalancedAccuracy
from brier import Brier


class Metrics(BaseModel):
    """All awailable metrics."""

    accuracy: MetricBase = Accuracy
    balanced_accuracy: MetricBase = BalancedAccuracy
    fbeta_score: MetricBase = FBeta
    rmse: MetricBase = RMSE
    mse: MetricBase = MSE
    recall: MetricBase = Recall
    precision: MetricBase = Precision
    average_precision: MetricBase = AveragePrecision
    brier: MetricBase = Brier


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
) -> Any:
    """Use given metric with non-default settings."""
    if metric_name not in all_metrics():
        print(f"Metric {metric_name} is not defined")
    else:
        metric = getattr(Metrics(), metric_name)
        return metric().calculate(expected, out)


print(f"accuracy fields: {Metrics().accuracy.model_fields}")
print(f"accuracy info: {metric_info('accuracy')}")
print(f"abc info: {metric_info('abc')}")
print(f"accuracy calculate: {calculate_default_metric('accuracy', [1,2,3], [1,2,3])}")
print(f"abc calculate: {calculate_default_metric('abc', [1,2,3], [1,2,3])}")
# print(f"test: {test().info()}")
