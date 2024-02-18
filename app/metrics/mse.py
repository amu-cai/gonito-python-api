from sklearn import metrics as sk_metrics


def mse(expected: list[float], out: list[float]) -> float:
    """
    Mean squared error metric.

    Parameters
    ----------
    expected : list[float]
        Path to the file with expected values.
    out : list[float]
        Path to the file with predicted values.

    Returns
    -------
    Value of the metric.
    """
    try:
        return sk_metrics.mean_squared_error(
            y_true=expected,
            y_pred=out,
        )
    except Exception as e:
        print(f"Could not calculate score because of error: {e}")
