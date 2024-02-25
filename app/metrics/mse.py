from sklearn import metrics as sk_metrics

from .metric_base import MetricBase


class MSE(MetricBase):
    """
    Mean squared error class.

    Parameters
    ----------
    sample_weight : list[float] | None, default None
        Sample weights.
    multioutput : str | list, default 'uniform_average'
        Defines aggregating of multiple output values. Values: ‘raw_values’,
        ‘uniform_average’.
    """

    sample_weight: list | None = None
    multioutput: str | list = "uniform_average"

    def info(self) -> dict:
        return {
            "name": "mean squared error",
            "link": "https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_squared_error.html#sklearn.metrics.mean_squared_error",
            "parameters": [
                "sample_weight: list | None (default None)",
                "multioutput str | list (default 'uniform_average');\
                    ‘raw_values’, ‘uniform_average’"
            ]
        }

    def calculate(
        self,
        expected: list[float],
        out: list[float],
    ) -> float | list[float]:
        """
        Metric calculation

        Parameters
        ----------
        expected : list[float]
            List with expected values.
        out : list[int]
            List with actual values.

        Returns
        -------
        Value of the metric.
        """
        try:
            return sk_metrics.mean_squared_error(
                y_true=expected,
                y_pred=out,
                sample_weight=self.sample_weight,
                multioutput=self.multioutput,
            )
        except Exception as e:
            print(f"Could not calculate score because of error: {e}")
