from pydantic import BaseModel

from .accuracy import Accuracy
from .mse import MSE
from .rmse import RMSE
from .fbeta_score import FBeta
from .recall import Recall
from .precision import Precision


class Metrics(BaseModel):
    """All awailable metrics."""
    accuracy = Accuracy.info()
    fbeta_score = FBeta.info()
    rmse = RMSE.info()
    mse = MSE.info()
    recall = Recall.info()
    precision = Precision.info()


"""
Pearson | Spearman | BLEU | GLEU | WER | CER
              | ClippEU
              | FMeasure Double | MacroFMeasure Double | NMI
              | LogLossHashed Word32 | CharMatch | MAP | NDCG Int | LogLoss
              | Likelihood
              | BIOF1 | BIOWeightedF1 | BIOF1Labels | TokenAccuracy
              | SegmentAccuracy | LikelihoodHashed Word32
              | PerplexityHashed Word32
              | MAE | SMAPE
              | MultiLabelFMeasure Double MatchingSpecification
              | MultiLabelLogLoss | MultiLabelLikelihood
              | SoftFMeasure Double
              | ProbabilisticMultiLabelFMeasure Double
              | ProbabilisticSoftFMeasure Double
              | ProbabilisticSoft2DFMeasure Double
              | Soft2DFMeasure Double
              | FLCFMeasure Double
              | Haversine
              | Improvement Double
              | Mean Metric
              | MacroAvg Metric
              | MAEAgainstInterval | MSEAgainstInterval | RMSEAgainstInterval
              | WAR | CAR

"""
