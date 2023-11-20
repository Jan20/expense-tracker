import csv
import pandas as pd
from pandas import DataFrame


def read_comdirect_file(file_path: str) -> DataFrame:
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

    # Resetting the index after dropping rows
    df = df.reset_index(drop=True)

    # Apply the conversion function to the 'Amount' column
    df['Umsatz in EUR'] = df['Umsatz in EUR'].str.replace('.', '').str.replace(',', '.').astype(float)

    return df


def read_american_express_file(file_path: str):
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
