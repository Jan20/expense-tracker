from typing import List

from application.domain.entities.expense import Expense
from application.domain.services.expense_service import ExpenseService
from application.use_cases.analysis_usecase import AnalysisUseCase
from pandas import DataFrame, to_datetime, concat

expense_service = ExpenseService()


class AnalysisService(AnalysisUseCase):
    months_to_int = {
        '01 January': 1,
        '02 February': 2,
        '03 March': 3,
        '04 April': 4,
        '05 May': 5,
        '06 June': 6,
        '07 July': 7,
        '08 August': 8,
        '09 September': 9,
        '10 October': 10,
        '11 November': 11,
        '12 December': 12,
    }

    def create_aggregated_expense_dataframe(self) -> DataFrame:
        """
        Creates

        @param timeframe: Specific year for which a chart gets generated
        @return: None
        """

        # Create an empty DataFrame with specific columns
        dataframe = DataFrame(columns=['description', 'amount', 'month'])

        original_df = self.create_expense_dataframe()

        for key, value in self.months_to_int.items():
            df = original_df.copy()
            df = df[df['date'].dt.month == value]

            # Replace the 'description' value if it contains the substring
            df['description'] = df['description'].apply(replace_description)

            df = df[df['description'] != 'Investments']
            df = df[df['description'] != 'American Express']

            # Group by 'Description' and 'Location' and sum the 'Amount'
            df = df.groupby(['description']).agg({'amount': 'sum'}).reset_index()
            if df.size > 0:
                df['month'] = key
                dataframe = concat(objs=[dataframe, df], ignore_index=True)

        return dataframe

    def create_expense_dataframe(self) -> DataFrame:
        expenses: List[Expense] = expense_service.get_expenses()

        # Create a DataFrame from the expense list
        df = DataFrame(expenses)

        # Convert the 'Date' column to datetime objects
        df['date'] = to_datetime(df['date'])

        # Drop rows where 'Amount' column has negative values
        df = df[df['amount'] >= 0]

        return df


def replace_description(description: str) -> str:
    replacements = {
        "AMZN": "Amazon",
        "AMAZON.DE": "Amazon",
        "LIEFERANDO": "Lieferando",
        "DEUTSCHEBAHN": "Deutsche Bahn",
        "REWE": "Rewe",
        "HEADSPACE": "Headspace",
        "MONATSGEBÜHR": "American Express",
        "SUMUP * HERR HASE": "Herr Hase",
        "GRAVIS": "Apple",
        "DER GUTE BAECKER": "Bakery",
        "Miete": "Rent",
        "Kontouebertrag": "Investments",
        "BOOKING": "Traveling",
        "American Express Europe": "American Express",
        "MINAMITSURU-GUN": "Japan Journey",
        "E WIE EINFACH": "e wie einfach",
        "HALLESCHE": "Hallische",
        "HOTEL": "Traveling",
        "Universitaet": "Hochschulsport"
    }

    for key, value in replacements.items():
        if key in description:
            return value

    return "Untracked"
