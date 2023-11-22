from abc import ABC, abstractmethod

from application.domain.entities.kpi import KPI


class KPIUseCase(ABC):

    @abstractmethod
    def calculate_key_performance_indicators(self) -> KPI:
        """ Calculates key performance indicators providing insights into
            a user's financial situation.
        """
        pass
