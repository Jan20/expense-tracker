from abc import ABC, abstractmethod


class FileUseCase(ABC):

    @abstractmethod
    def get_files(self, dir_name: str) -> [str]:
        """Get all file names in the specified directory"""
        pass

    @abstractmethod
    def import_files(self, dir_name: str) -> bool:
        """Create a new expense and return the created expense entity."""
        pass
