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

    def create_monthly_expenses_dataframe(self) -> DataFrame:
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
            df['month'] = key

            if not df.empty:
                dataframe = concat(objs=[dataframe, df], ignore_index=True)

        return dataframe

    def create_yearly_expenses_dataframe(self) -> DataFrame:
        # Create an empty DataFrame with specific columns
        df = self.create_expense_dataframe()

        # Replace the 'description' value if it contains the substring
        df['description'] = df['description'].apply(replace_description)

        df = df[df['description'] != 'Investments']
        df = df[df['description'] != 'American Express']

        # Group by 'Description' and 'Location' and sum the 'Amount'
        df = df.groupby(['description']).agg({'amount': 'sum'}).reset_index()
        print(df.to_string())
        return df

    def create_expense_dataframe(self) -> DataFrame:
        # Create a DataFrame from the expense list
        df = DataFrame(expense_service.get_expenses())

        # Convert the 'Date' column to datetime objects
        df['date'] = to_datetime(df['date'])

        # Drop rows where 'Amount' column has negative values
        df = df[df['amount'] >= 0]
        print(df.to_string())
        return df

    def compute_total_expenses(self) -> float:
        df = self.create_expense_dataframe()
        return df['amount'].sum()


def replace_description(description: str) -> str:
    replacements = {
        "APPLE": "apple",
        "AMZN": "Amazon",
        "AMAZON.DE": "Amazon",
        "Rundfunk": "GEZ",
        "AXA": "Haftpflicht",
        "flaschenpost": "Flaschenpost",
        "AUDIBLE": "Audible",
        "LONDON": "Traveling",
        "LIEFERANDO": "Lieferando",
        "AUSLANDSENTGELT": "AUSLANDSENTGELT",
        "Takeaway": "Lieferando",
        "DEUTSCHEBAHN": "Deutsche Bahn",
        "REWE": "Rewe",
        "HEADSPACE": "Headspace",
        "MONATSGEBÜHR": "American Express",
        "HERR HASE": "Herr Hase",
        "VODAFONE": "Vodafone",
        "MAGNOLIA": "Magnolia",
        "GRAVIS": "Apple",
        "DER GUTE BAECKER": "Bakery",
        "Miete": "Rent",
        "Kontouebertrag": "Investments",
        "EUROWINGS": "Traveling",
        "BOOKING": "Traveling",
        "American Express Europe": "American Express",
        "MINAMITSURU-GUN": "Japan Journey",
        "ABSCHLAG Strom": "Strom",
        "ABSCHLAG Gas": "Gas",
        "HALLESCHE": "Hallische",
        "HOTEL": "Traveling",
        "Universitaet": "Hochschulsport",
        "Bargeldauszahlung": "Cash",
        "Zahnarztpraxis": "Dentist",
        "Sanitaer": "Craftsmans",
        "Galactica": "Going Out",
    }

    for key, value in replacements.items():
        if key in description:
            return value

    return "Untracked"
