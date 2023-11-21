from abc import ABC, abstractmethod
from pandas import DataFrame


class AnalysisUseCase(ABC):

    @abstractmethod
    def create_monthly_expenses_dataframe(self) -> DataFrame:
        """
        Creates a dataframe containing the aggregated expenses on a monthly basis, sorted by category.

        @return: DataFrame containing the aggregated expenses
        """
        pass

    @abstractmethod
    def create_yearly_expenses_dataframe(self) -> DataFrame:
        """
        Creates a dataframe containing the aggregated expenses on a monthly basis, sorted by category.

        @return: DataFrame containing the aggregated expenses
        """
        pass

    @abstractmethod
    def create_expense_dataframe(self) -> DataFrame:
        """
        Constructs an expense dataframe

        @return: None
        """
        pass

    @abstractmethod
    def compute_total_expenses(self) -> float:
        """
        Computes the total expenses

        @return: None
        """
        pass
