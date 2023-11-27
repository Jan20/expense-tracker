from datetime import datetime
from os import listdir
from os.path import isfile, join, isdir, exists
from typing import List

from application.domain.services.expense_service import ExpenseService
from application.domain.services.income_service import IncomeService
from application.domain.utils.utils import read_comdirect_file, read_american_express_file
from application.use_cases.file_usecase import FileUseCase
from pandas import DataFrame

expense_service = ExpenseService()
income_service = IncomeService()


class FileService(FileUseCase):

    def get_files(self, directory: str) -> [str]:
        """Get all file names in the specified directory"""
        if not isdir(directory):
            raise ValueError(f"The specified directory '{directory}' does not exist.")

        return [file for file in listdir(directory) if isfile(join(directory, file))]

    def import_expenses_from_file(self, directory: str) -> str:
        # Delete all previously stored expenses
        expense_service.delete_expenses()

        comdirect_file_path = join(directory, 'comdirect.csv')

        if exists(comdirect_file_path):
            comdirect_file = read_comdirect_file(file_path=comdirect_file_path)
            self.import_comdirect_expenses(df=comdirect_file)

        american_express_file_path = join(directory, 'american_express.csv')

        if exists(american_express_file_path):
            american_express_file = read_american_express_file(file_path=american_express_file_path)
            self.import_american_express_expenses(file=american_express_file)

        return "Expenses imported"

    def import_incomes_from_file(self, directory: str) -> str:
        # Delete all previously stored expenses
        income_service.delete_incomes()

        comdirect_file_path = join(directory, 'comdirect.csv')

        if exists(comdirect_file_path):
            comdirect_file = read_comdirect_file(file_path=comdirect_file_path)
            self.import_comdirect_incomes(comdirect_file)

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

    def import_comdirect_incomes(self, df: DataFrame):
        df = df[df['Umsatz in EUR'] > 0]

        for index, row in df.iterrows():
            income_service.create_income(
                date=datetime.strptime(row['Buchungstag'], '%d.%m.%Y'),
                description=row['Buchungstext'],
                amount=float(row['Umsatz in EUR'])
            )