from abc import ABC, abstractmethod


class ChartUseCase(ABC):

    @abstractmethod
    def generate_expense_chart(self, year: int) -> None:
        """
        Generate an expense chart for a given year

        @param year: Specific year for which a chart gets generated
        @return: None
        """
        pass
