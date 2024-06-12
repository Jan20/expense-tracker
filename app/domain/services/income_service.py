import io
import locale
import os

from matplotlib.figure import Figure
from pandas import DataFrame
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer
from reportlab.platypus import Table

from app.domain.entities.enums import TransactionType
from app.domain.entities.styles import DEFAULT_STYLE
from app.domain.services.transaction_service import TransactionService


class IncomeService:
    def __init__(self, transaction_service: TransactionService):
        self.transaction_service: TransactionService = transaction_service

    def create_income_summary(self, year: int) -> SimpleDocTemplate:
        df = self.transaction_service.get_transaction_dataframe(
            year=year,
            transaction_type=TransactionType.INCOME,
        )
        df = self.__adjust_dataframe(df)

        return SimpleDocTemplate(filename="files/income_summary.pdf", pagesize=A4).build(
            flowables=[
                self.__create_headline(year),
                self.__create_table(df),
                Spacer(width=1, height=1),
                self.__create_graph(df)
            ],
            onFirstPage=self.__create_logo,
            onLaterPages=self.__create_logo
        )

    @staticmethod
    def __create_logo(canvas: Canvas, _: SimpleDocTemplate):
        png_path = os.path.join("./files/logo.png")
        canvas.saveState()
        canvas.drawImage(png_path, x=505, y=750, width=100, height=100)
        canvas.restoreState()

    @staticmethod
    def __create_table(df: DataFrame) -> Table:
        df = df.groupby('description')['amount'].sum().reset_index()
        df = df.sort_values(by='amount', ascending=False)
        df['percentage'] = (df['amount'] / df['amount'].sum()) * 100

        df.loc[len(df)] = {
            'description': 'SUM',
            'amount': df['amount'].sum(),
            'percentage': df["percentage"].sum(),
        }

        df['percentage'] = df['percentage'].map(lambda x: f'{x:.2f} %')
        df['amount'] = df['amount'].map(lambda x: locale.currency(x, symbol=True, grouping=True, international=True))
        return Table([['Description', 'Amount', 'Percentage']] + df.values.tolist(), colWidths=145, style=DEFAULT_STYLE)

    @staticmethod
    def __create_headline(year: int) -> Paragraph:
        return Paragraph(
            text=f'Income Summary {year}',
            style=ParagraphStyle(
                name='Headline',
                fontSize=24,
                leading=28,
                spaceAfter=12
            )
        )

    @staticmethod
    def __create_graph(df: DataFrame) -> Image:
        df = df.resample(rule='ME', on='date')['amount'].sum()

        figure = Figure()
        ax = figure.subplots()
        ax.bar(df.index.strftime('%b'), df, align='center', color='green', label='Incomes')
        ax.set_xlabel('Month')
        ax.set_ylabel('Incomes')
        ax.legend()

        buffer = io.BytesIO()
        figure.savefig(buffer, format="png", dpi=600)
        buffer.seek(0)
        return Image(buffer, width=480, height=360)

    def __adjust_dataframe(self, df: DataFrame) -> DataFrame:
        df['description'] = df['description'].map(self.__replace_description)
        mask = ~df['description'].isin(['American Express', 'Investments'])
        df = df.loc[mask]
        return df

    @staticmethod
    def __replace_description(description: str) -> str:
        replacements = {
            "Lina": "Lina",
            "Lohn/Gehalt": "Salary",
            "HALLESCHE": "Health Insurance",
            "DB Vertrieb": "Deutsche Bahn Refunds",
            "STEUERVERWALTUNG": "Tax Refund",
            "AMAZON": "Refunds",
            "AMZNPRIME": "Refunds",
            "AMZN": "Refunds",
            "flaschenpost": "Refunds",
        }

        for key, value in replacements.items():
            if key in description:
                return value

        return "Unsorted"
