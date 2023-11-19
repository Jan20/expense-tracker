from abc import ABC, abstractmethod


class ReportUseCase(ABC):

    @abstractmethod
    def generate_financial_report(self, year: int):
        """Generate a financial report for a given year"""
        pass
