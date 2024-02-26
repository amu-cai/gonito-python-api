from sklearn import metrics as sk_metrics

from .metric_base import MetricBase


class AveragePrecision(MetricBase):
    """
    Average precision metric.

    Parameters
    ----------
    pos_label : int | float | bool | str, default 1
        The class to report if average='binary' and the data is binary.
    average : str | None, default 'macro'
        This parameter is required for multiclass/multilabel targets. Values:
        ‘micro’, ‘macro’, ‘samples’, ‘weighted’ or None.
    sample_weight : list[float] | None, default None
        Sample weights.
    zero_division : str | float | np.NaN, default 'warn'
        Sets the value to return when there is a zero division, i.e. when all
        predictions and labels are negative. Values: “warn”, 0.0, 1.0, np.nan.
    """

    pos_label: int | float | bool | str = 1
    average: str | None = 'bianry'
    sample_weight: list | None = None

    def info(self) -> dict:
        return {
            "name": "average precision",
            "link": "https://scikit-learn.org/stable/modules/generated/sklearn.metrics.average_precision_score.html#sklearn.metrics.average_precision_score",
            "parameters": [
                "pos_label: int | float | bool | str (default 1)",
                "average : str | None (default 'macro'); ‘micro’, ‘macro’,\
                        ‘samples’, ‘weighted’",
                "sample_weight: list | None (default None)"
            ]
        }

    def precision(
        self,
        expected: list[int],
        out: list[int]
    ) -> float | list[float]:
        """
        Metric calculation

        Parameters
        ----------
        expected : list[int]
            List with expected values.
        out : list[int]
            List with actual values.

        Returns
        -------
        Value of the metric.
        """
        try:
            return sk_metrics.average_precision_score(
                y_true=expected,
                y_pred=out,
                pos_label=self.pos_label,
                average=self.average,
                sample_weight=self.sample_weight,
            )
        except Exception as e:
            print(f"Could not calculate score because of error: {e}")
