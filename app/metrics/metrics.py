from sklearn.metrics import accuracy_score
from typing import List


# TODO change to dataclass and then implement method to dupm everythnig to list
class Metrics:
    ACCURACY: str = "accuracy"
    F1: str = "f1"

    def get_all(self):
        return ["f1", "accuracy"]


def accuracy(true: List[int | float], pred: List[int | float]) -> float:
    return accuracy_score(true, pred)
