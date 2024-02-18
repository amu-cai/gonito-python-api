from sklearn import metrics as sk_metrics


def fbeta_score(expected: list[int], out: list[int], beta: int) -> float:
    """
    F-beta score metric.

    Parameters
    ----------
    expected : list[int]
        Path to the file with expected values.
    out : list[int]
        Path to the file with predicted values.
    beta : int
        Ratio of recall importance to precision importance. beta > 1 gives more
        weight to recall, while beta < 1 favors precision.

    Returns
    -------
    Value of the metric.
    """
    try:
        return sk_metrics.fbeta_score(
            y_true=expected,
            y_pred=out,
            beta=beta,
        )
    except Exception as e:
        print(f"Could not calculate score because of error: {e}")
