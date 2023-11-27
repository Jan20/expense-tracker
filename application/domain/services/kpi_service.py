from application.domain.entities.kpi import KPI
from application.domain.services.expense_analysis_service import ExpenseAnalysisService
from application.domain.services.income_analysis_service import IncomeAnalysisService
from application.use_cases.kpi_usecase import KPIUseCase

income_analysis_service = IncomeAnalysisService()
expense_analysis_service = ExpenseAnalysisService()


class KPIService(KPIUseCase):

    def calculate_key_performance_indicators(self) -> KPI:
        total_income = income_analysis_service.compute_total_income()
        total_expenses = expense_analysis_service.compute_total_expenses()
        total_savings = total_income-total_expenses

        return KPI(
            total_income=total_income,
            total_expenses=total_expenses,
            total_savings=total_savings,
            savings_rate=self.calculate_savings_rate(total_income, total_savings)
        )

    def calculate_savings_rate(self, total_income: float, total_savings: float):
        if total_income == 0:
            return 0
        return (total_savings / total_income) * 100
