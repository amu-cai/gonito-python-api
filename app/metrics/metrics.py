from pydantic import BaseModel

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
