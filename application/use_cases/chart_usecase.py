from abc import ABC, abstractmethod


class ChartUseCase(ABC):

    @abstractmethod
    def generate_monthly_expenses_chart(self) -> None:
        """
        Generate an expense chart for a given year

        @return: None
        """
        pass

    @abstractmethod
    def generate_yearly_expenses_chart(self) -> None:
        """
        Generate an expense chart for a given year

        @return: None
        """
        pass
