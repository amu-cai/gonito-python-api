from pydantic import BaseModel

from .accuracy import Accuracy
from .mse import MSE
from .rmse import RMSE
from .fbeta_score import FBeta
from .recall import Recall
from .precision import Precision
from .average_precision import AveragePrecision


class Metrics(BaseModel):
    """All awailable metrics."""
    accuracy = Accuracy.info()
    fbeta_score = FBeta.info()
    rmse = RMSE.info()
    mse = MSE.info()
    recall = Recall.info()
    precision = Precision.info()
    average_precision = AveragePrecision.info()
