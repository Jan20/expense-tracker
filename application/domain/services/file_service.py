from datetime import datetime
from os import listdir
from os.path import isfile, join, isdir
from typing import List

from application.domain.services.expense_service import ExpenseService
from application.domain.utils.utils import read_comdirect_file, read_american_express_file
from application.use_cases.file_usecase import FileUseCase
from pandas import DataFrame

expense_service = ExpenseService()


class FileService(FileUseCase):

    def get_files(self, directory: str) -> [str]:
        """Get all file names in the specified directory"""
        if not isdir(directory):
            raise ValueError(f"The specified directory '{directory}' does not exist.")

        return [file for file in listdir(directory) if isfile(join(directory, file))]

    def import_files(self, directory: str) -> str:
        # Delete all previously stored expenses
        expense_service.delete_expenses()

        # Read data from the CSV file
        comdirect_file = read_comdirect_file(join(directory, 'comdirect.csv'))

        self.import_comdirect_expenses(comdirect_file)

        # Read data from the CSV file
        american_express_file = read_american_express_file(join(directory, 'american_express.csv'))

        self.import_american_express_expenses(american_express_file)

        return "Files imported"

    def import_american_express_expenses(self, file: List[dict]):
        for row in file:
            expense_service.create_expense(
                date=datetime.strptime(row['Datum'], '%d/%m/%Y'),
                description=row['Beschreibung'],
                amount=float(row['Betrag'].replace(',', '.'))
            )

    def import_comdirect_expenses(self, df: DataFrame):
        df['Umsatz in EUR'] = df['Umsatz in EUR'].apply(lambda x: -x)

        for index, row in df.iterrows():
            expense_service.create_expense(
                date=datetime.strptime(row['Buchungstag'], '%d.%m.%Y'),
                description=row['Buchungstext'],
                amount=float(row['Umsatz in EUR'])
            )
