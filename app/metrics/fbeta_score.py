from sklearn import metrics as sk_metrics

from .metric_base import MetricBase


class FBeta(MetricBase):
    """
    F-beta score class.

    Parameters
    ----------
    beta : float, default 1.0
        Ratio of recall importance to precision importance. beta > 1 gives more
        weight to recall, while beta < 1 favors precision.
    labels : list | None, default None
        The set of labels to include.
    pos_label : int | float | bool | str, default 1
        The class to report if average is binary and the data is binary.
    average : str | None, default 'binary'
        Possible values: ‘micro’, ‘macro’, ‘samples’, ‘weighted’, ‘binary’.
    sample_weight : list | None, default None
        Sample weights.
    zero_division : str | float | np.NaN, default 'warn'
        Sets the value to return when there is a zero division, i.e. when all
        predictions and labels are negative. Values: “warn”, 0.0, 1.0, np.nan.
    """

    beta: float = 1.0
    labels: list | None = None
    pos_label: int | float | bool | str = 1
    average: str | None = "binary"
    sample_weight: list | None = None
    zero_division: str | float = 'warn'

    def info(self) -> dict:
        return {
            "name": "f-beta score",
            "link": "https://scikit-learn.org/stable/modules/generated/sklearn.metrics.fbeta_score.html#sklearn.metrics.fbeta_score",
            "parameters": [
                "beta: float (default 1.0)",
                "labels: list (default None)",
                "pos_label: int | float | bool | str (default 1)",
                "average: str | None (default 'binary');\
                    ‘micro’, ‘macro’, ‘samples’, ‘weighted’, ‘binary’",
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
            return sk_metrics.fbeta_score(
                y_true=expected,
                y_pred=out,
                beta=self.beta,
                labels=self.labels,
                pos_label=self.pos_label,
                average=self.average,
                sample_weight=self.sample_weight,
                zero_division=self.zero_division,
            )
        except Exception as e:
            print(f"Could not calculate score because of error: {e}")
