from abc import ABC, abstractmethod


class MetricBase(ABC):
    """Base class for all metrics."""

    @abstractmethod
    def calculate(self):
        pass

    @abstractmethod
    def info(self) -> dict:
        pass
