from pydantic import BaseModel

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
