from abc import ABC, abstractmethod
from pandas import DataFrame


class AnalysisUseCase(ABC):

    @abstractmethod
    def create_aggregated_expense_dataframe(self) -> DataFrame:
        """
        Creates a dataframe with

        @param timeframe: Specific year for which a chart gets generated
        @return: None
        """
        pass

    @abstractmethod
    def create_expense_dataframe(self) -> DataFrame:
        """
        Constructs an expense dataframe

        @return: None
        """
        pass

