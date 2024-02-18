from sklearn import metrics as sk_metrics


def accuracy(expected: list[int], out: list[int]) -> float:
    """
    Accuracy metric.

    Parameters
    ----------
    expected : list[int]
        Path to the file with expected values.
    out : list[int]
        Path to the file with predicted values.

    Returns
    -------
    Value of the metric.
    """
    try:
        return sk_metrics.accuracy_score(
            y_true=expected,
            y_pred=out,
        )
    except Exception as e:
        print(f"Could not calculate score because of error: {e}")
