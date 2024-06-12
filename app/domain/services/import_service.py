import csv
from datetime import datetime
from os.path import isdir, exists
from pathlib import Path
from typing import List

import pandas as pd
from flask import abort
from pandas import DataFrame

from app.domain.services.transaction_service import TransactionService


class ImportService:
    def __init__(self, transaction_service: TransactionService):
        self.transaction_service: TransactionService = transaction_service

    @staticmethod
    def get_files(directory: str) -> [str]:
        """Get all file names in the specified directory"""
        if not isdir(directory):
            raise ValueError(f"The specified directory '{directory}' does not exist.")

        path_list = Path(directory).rglob('*')
        return [str(path) for path in path_list if path.is_file() and path.name != '.DS_Store']

    def import_transactions_from_files(self, file_paths: [str]):
        self.transaction_service.delete_transactions()

        for file_path in file_paths:
            self.__import_transactions_from_file(file_path)

        return "Transactions successfully imported"

    def __import_transactions_from_file(self, file_path: str) -> str:

        if not exists(file_path):
            abort(400, description=f'{file_path} does not exist')

        if 'american_express' in file_path:
            american_express_file = self.__read_american_express_file(file_path=file_path)
            self.__import_american_express_transactions(file=american_express_file)

        if 'comdirect' in file_path:
            comdirect_file = self.__read_comdirect_file(file_path=file_path)
            self.__import_comdirect_transactions(df=comdirect_file)

        return "Transaction successfully imported"

    def __import_american_express_transactions(self, file: List[str]):
        for row in file:
            self.transaction_service.create_transaction(
                date=datetime.strptime(row['Datum'], '%d/%m/%Y'),
                description=row['Beschreibung'],
                amount=float(row['Betrag'].replace(',', '.')) * -1
            )

    def __import_comdirect_transactions(self, df: DataFrame):
        for index, row in df.iterrows():
            self.transaction_service.create_transaction(
                date=datetime.strptime(row['Buchungstag'], '%d.%m.%Y'),
                description=row['Buchungstext'],
                amount=float(row['Umsatz in EUR'])
            )

    @staticmethod
    def __read_comdirect_file(file_path: str) -> DataFrame:
        """
        Reads a CSV file and returns the data as a list of dictionaries.

        Parameters:
        - file_path (str): The path to the CSV file.

        Returns:
        - list of dict: A list of dictionaries where each dictionary represents a row in the CSV file.
        """
        df = pd.read_csv(file_path, sep=';', encoding='latin-1', skipfooter=2, skiprows=4, engine='python')
        df = df.drop(columns='Wertstellung (Valuta)')
        df = df.drop(columns=['Unnamed: 5'])
        df = df[df['Buchungstag'] != 'offen']
        df = df.reset_index(drop=True)
        df['Umsatz in EUR'] = df['Umsatz in EUR'].str.replace('.', '').str.replace(',', '.').astype(float)
        return df

    @staticmethod
    def __read_american_express_file(file_path: str):
        """
        Reads a CSV file and returns the data as a list of dictionaries.

        Parameters:
        - file_path (str): The path to the CSV file.

        Returns:
        - list of dict: A list of dictionaries where each dictionary represents a row in the CSV file.
        """
        data = []
        with open(file_path, 'r', newline='', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                data.append(row)
        return data

