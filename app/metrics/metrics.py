from pydantic import BaseModel


class Metrics(BaseModel):
    """All awailable metrics."""
    accuracy = "accuracy"
    fbeta_score = "fbeta_score"
    rmse = "rmse"
    mse = "mse"
    recall = "recall"
    precision = "precision"


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
