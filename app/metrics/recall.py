from sklearn import metrics as sk_metrics


def recall(expected: list[int], out: list[int]) -> float:
    """
    Recall metric.

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
        return sk_metrics.recall_score(
            y_true=expected,
            y_pred=out,
        )
    except Exception as e:
        print(f"Could not calculate score because of error: {e}")
