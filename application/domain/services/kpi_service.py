from application.use_cases.kpi_usecase import KPIUseCase
from pandas import DataFrame


class KPIService(KPIUseCase):

    def calculate_key_performance_indicators(self) -> DataFrame:
        pass
