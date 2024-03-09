from pydantic import BaseModel
from abc import ABC, abstractmethod


class MetricBase(BaseModel, ABC):
    """Base class for all metrics."""

    @abstractmethod
    def calculate(self):
        pass

    @abstractmethod
    def info(self) -> dict:
        pass
