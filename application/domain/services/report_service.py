from application.domain.services.chart_service import ChartService
from application.domain.services.expense_analysis_service import ExpenseAnalysisService
from application.domain.services.income_analysis_service import IncomeAnalysisService
from application.use_cases.report_usecase import ReportUseCase

chart_service = ChartService()
expense_analysis_service = ExpenseAnalysisService()
income_analysis_service = IncomeAnalysisService()


class ReportService(ReportUseCase):

    def generate_financial_report(self, year: int):
        """Generates a financial report for a given year."""
        df = expense_analysis_service.create_yearly_expenses_dataframe()
        chart_service.generate_aggregated_chart(df)

        df = income_analysis_service.create_yearly_income_dataframe()
        chart_service.generate_aggregated_chart(df)

