import os
from datetime import datetime
from os.path import isfile, join

from application.domain.services.expense_service import ExpenseService
from application.domain.utils.utils import read_csv_file
from application.use_cases.file_usecase import FileUseCase

expense_service = ExpenseService()


class FileService(FileUseCase):

    def get_files(self, directory: str) -> [str]:
        """Get all file names in the specified directory"""
        if not os.path.isdir(directory):
            raise ValueError(f"The specified directory '{directory}' does not exist.")

        return [file for file in os.listdir(directory) if isfile(join(directory, file))]

    def import_files(self, directory: str) -> str:

        expense_service.delete_expenses()

        files: [str] = self.get_files(directory=directory)

        file_path = join(directory, files[0])

        data = read_csv_file(file_path)

        entities = []

        for entry in data:
            # Convert 'Datum' to datetime
            timestamp = datetime.strptime(entry['Datum'], '%d/%m/%Y')

            description = entry["Beschreibung"]

            # Convert 'Betrag' to float
            amount = float(entry['Betrag'].replace(',', '.'))

            expense_service.create_expense(
                timestamp=timestamp,
                description=description,
                amount=amount
            )

        print(entities)

        return file_path
