from sklearn import metrics as sk_metrics

from .metric_base import MetricBase


class Recall(MetricBase):
    """
    Recall metric class.

    Parameters
    ----------
    labels : list, default None
        The set of labels.
    pos_label : int | float | bool | str, default 1
        The class to report if average='binary' and the data is binary.
    average : str | None, default 'bianry'
        This parameter is required for multiclass/multilabel targets. Values:
        ‘micro’, ‘macro’, ‘samples’, ‘weighted’, ‘binary’ or None.
    sample_weight : list[float] | None, default None
        Sample weights.
    zero_division : str | float | np.NaN, default 'warn'
        Sets the value to return when there is a zero division, i.e. when all
        predictions and labels are negative. Values: “warn”, 0.0, 1.0, np.nan.
    """

    labels: list | None = None
    pos_label: int | float | bool | str = 1
    average: str | None = 'bianry'
    sample_weight: list | None = None
    zero_division: str | float = 'warn'

    def info(self) -> dict:
        return {
            "name": "recall",
            "link": "https://scikit-learn.org/stable/modules/generated/sklearn.metrics.recall_score.html#sklearn.metrics.recall_score",
            "parameters": [
                "labels: list | None (default None)",
                "pos_label: int | float | bool | str (default 1)",
                "average : str | None (default 'bianry'); ‘micro’, ‘macro’,\
                        ‘samples’, ‘weighted’, ‘binary’",
                "sample_weight: list | None (default None)",
                "zero_division : str | float | np.NaN (default 'warn')"
            ]
        }

    def calculate(
        self,
        expected: list[int],
        out: list[int],
    ) -> float | list[float]:
        """
        Metric calculation.

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
            return sk_metrics.recall_score(
                y_true=expected,
                y_pred=out,
                labels=self.labels,
                pos_label=self.pos_label,
                average=self.average,
                sample_weight=self.sample_weight,
                zero_division=self.zero_division,
            )
        except Exception as e:
            print(f"Could not calculate score because of error: {e}")
