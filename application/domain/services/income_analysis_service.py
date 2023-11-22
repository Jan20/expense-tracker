from pandas import DataFrame, to_datetime, concat

from application.domain.services.income_service import IncomeService
from application.use_cases.income_analysis_usecase import IncomeAnalysisUseCase

income_service = IncomeService()


class IncomeAnalysisService(IncomeAnalysisUseCase):
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

    def create_monthly_income_dataframe(self) -> DataFrame:
        dataframe = DataFrame(columns=['description', 'amount', 'month'])

        original_df = self.create_income_dataframe()

        for key, value in self.months_to_int.items():
            df = original_df.copy()
            df = df[df['date'].dt.month == value]

            df['description'] = df['description'].apply(replace_description)

            df = df[df['description'] != 'Investments']
            df = df[df['description'] != 'American Express']

            df = df.groupby(['description']).agg({'amount': 'sum'}).reset_index()
            df['month'] = key

            if not df.empty:
                dataframe = concat(objs=[dataframe, df], ignore_index=True)

        return dataframe

    def create_yearly_income_dataframe(self) -> DataFrame:
        df = self.create_income_dataframe()

        df['description'] = df['description'].apply(replace_description)

        df = df[df['description'] != 'Investments']
        df = df[df['description'] != 'American Express']

        df = df.groupby(['description']).agg({'amount': 'sum'}).reset_index()

        return df

    def create_income_dataframe(self) -> DataFrame:
        df = DataFrame(income_service.get_incomes())

        df['date'] = to_datetime(df['date'])

        df = df[df['amount'] < 0]

        return df

    def compute_total_income(self) -> float:
        df = self.create_income_dataframe()
        return df['amount'].sum()


def replace_description(description: str) -> str:
    replacements = {
        "APPLE": "apple",
    }

    for key, value in replacements.items():
        if key in description:
            return value

    return "Untracked"
