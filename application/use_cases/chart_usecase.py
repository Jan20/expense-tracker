from abc import ABC, abstractmethod
from pandas import DataFrame


class ChartUseCase(ABC):

    @abstractmethod
    def generate_monthly_expenses_chart(self, df: DataFrame) -> None:
        """
        Generate an expense chart for a given year

        @return: None
        """
        pass

    @abstractmethod
    def generate_aggregated_chart(self, df: DataFrame) -> None:
        """
        Generate an expense chart for a given year

        @return: None
        """
        pass
