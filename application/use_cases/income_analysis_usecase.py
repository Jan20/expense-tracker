from abc import ABC, abstractmethod
from pandas import DataFrame


class IncomeAnalysisUseCase(ABC):

    @abstractmethod
    def create_monthly_income_dataframe(self) -> DataFrame:
        """
        Creates a dataframe containing the aggregated income on a monthly basis, sorted by category.

        @return: DataFrame containing the aggregated income
        """
        pass

    @abstractmethod
    def create_yearly_income_dataframe(self) -> DataFrame:
        """
        Creates a dataframe containing the aggregated income on a monthly basis, sorted by category.

        @return: DataFrame containing the aggregated income
        """
        pass

    @abstractmethod
    def create_income_dataframe(self) -> DataFrame:
        """
        Constructs an income dataframe

        @return: None
        """
        pass

    @abstractmethod
    def compute_total_income(self) -> float:
        """
        Computes the total income

        @return: None
        """
        pass
