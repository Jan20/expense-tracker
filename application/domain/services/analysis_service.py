from typing import List

from application.domain.entities.expense import Expense
from application.domain.services.expense_service import ExpenseService
from application.use_cases.analysis_usecase import AnalysisUseCase
from pandas import DataFrame, to_datetime, concat

expense_service = ExpenseService()


class AnalysisService(AnalysisUseCase):
    months_to_int = {
        'December': 11,
        'November': 10,
        'October': 9,
        'September': 8,
        'August': 7,
        'July': 6,
        'June': 5,
        'May': 4,
        'April': 3,
        'March': 2,
        'February': 1,
        'January': 0
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
        print(original_df.to_string())

        for key, value in self.months_to_int.items():
            df = original_df.copy()
            df = df[df['timestamp'].dt.month == value]

            # Replace the 'description' value if it contains the substring
            df['description'] = df['description'].apply(replace_description)

            # Group by 'Description' and 'Location' and sum the 'Amount'
            df = df.groupby(['description']).agg({'amount': 'sum'}).reset_index()
            df['month'] = key

            if df.size > 0:
                dataframe = concat(objs=[dataframe, df], ignore_index=True)

        return dataframe

    def create_expense_dataframe(self) -> DataFrame:
        expenses: List[Expense] = expense_service.get_expenses()

        # Create a DataFrame from the expense list
        df = DataFrame(expenses)

        # Convert the 'Date' column to datetime objects
        df['timestamp'] = to_datetime(df['timestamp'])

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
    }

    for key, value in replacements.items():
        if key in description:
            return value

    return "Untracked"
