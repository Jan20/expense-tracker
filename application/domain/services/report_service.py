from application.domain.services.chart_service import ChartService
from application.use_cases.report_usecase import ReportUseCase

chart_service = ChartService()


class ReportService(ReportUseCase):

    def generate_financial_report(self, year: int):
        """Generates a financial report for a given year."""
        chart_service.generate_expense_chart(year=year)
