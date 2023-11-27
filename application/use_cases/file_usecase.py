from abc import ABC, abstractmethod
from typing import List
from pandas import DataFrame


class FileUseCase(ABC):

    @abstractmethod
    def get_files(self, directory: str) -> [str]:
        """ Get all file names in the specified directory. """
        pass

    @abstractmethod
    def import_expenses_from_file(self, file_path: str) -> bool:
        """ Create a new expense and return the created expense entity. """
        pass

    @abstractmethod
    def import_incomes_from_file(self, file_path: str) -> bool:
        """ Create a new expense and return the created expense entity. """
        pass

    @abstractmethod
    def import_american_express_expenses(self, file: List[dict]) -> None:
        """ Imports expenses from an American Express file. """
        pass

    @abstractmethod
    def import_comdirect_expenses(self, df: DataFrame) -> bool:
        """ Imports expenses from a Comdirect file. """
        pass

    @abstractmethod
    def import_comdirect_incomes(self, df: DataFrame) -> bool:
        """ Imports incomes from a Comdirect file. """
        pass
