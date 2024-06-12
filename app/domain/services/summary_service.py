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


class SummaryService:
    def __init__(self, transaction_service: TransactionService):
        self.transaction_service: TransactionService = transaction_service

    def create_summary(self, year: int) -> SimpleDocTemplate:
        """
        Generates a financial report for a given year.
        """
        return SimpleDocTemplate(filename="files/summary.pdf", pagesize=A4).build(
            flowables=[
                self.__create_headline(year=year),
                self.__generate_kpi_table(year=year),
                Spacer(width=1, height=1),
                self.__create_graph(year=year)
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

    def __create_graph(self, year: int) -> Image:
        income_df = self.transaction_service.get_transaction_dataframe(
            year=year,
            transaction_type=TransactionType.INCOME,
        )
        income_df = self.__adjust_dataframe(income_df)
        income_df = income_df.resample(rule='ME', on='date')['amount'].sum()

        expense_df = self.transaction_service.get_transaction_dataframe(
            year=year,
            transaction_type=TransactionType.EXPENSE,
        )
        expense_df = self.__adjust_dataframe(expense_df)
        expense_df = expense_df.resample(rule='ME', on='date')['amount'].sum()

        figure = Figure()
        ax = figure.subplots()

        ax.bar(income_df.index.strftime('%b'), income_df, align='center', color='green', label='Income')
        ax.bar(income_df.index.strftime('%b'), expense_df, align='center', color='#8B0000', label='Expenses')

        ax.set_xlabel('date')
        ax.set_ylabel('amount')
        ax.legend()

        buffer = io.BytesIO()
        figure.savefig(buffer, format="png", dpi=600)
        return Image(buffer, width=480, height=300)

    @staticmethod
    def __create_headline(year: int) -> Paragraph:
        return Paragraph(
            text=f'Financial Report {year}',
            style=ParagraphStyle(
                name='Headline',
                fontSize=24,
                leading=28,
                spaceAfter=12
            )
        )

    def __adjust_dataframe(self, df: DataFrame) -> DataFrame:
        df['description'] = df['description'].map(self.__replace_description)
        mask = ~df['description'].isin(['American Express', 'Investments'])
        df = df.loc[mask]
        return df

    def __generate_kpi_table(self, year: int) -> Table:
        income_df = self.transaction_service.get_transaction_dataframe(
            year=year,
            transaction_type=TransactionType.INCOME,
        )
        income_df = self.__adjust_dataframe(income_df)
        total_income = income_df['amount'].sum()

        expense_df = self.transaction_service.get_transaction_dataframe(
            year=year,
            transaction_type=TransactionType.EXPENSE,
        )
        expense_df = self.__adjust_dataframe(expense_df)
        expense_df.loc[:, 'amount'] = -expense_df['amount']
        total_expenses = expense_df['amount'].sum()

        total_savings = total_income - total_expenses

        data = [
            ["Income", "Expenses", "Total Savings", "Savings Rate"],
            [
                locale.currency(total_income, symbol=True, grouping=True, international=True),
                locale.currency(total_expenses, symbol=True, grouping=True, international=True),
                locale.currency(total_savings, symbol=True, grouping=True, international=True),
                f'{self.__calculate_savings_rate(total_income, total_savings) * 100:.2f} %',
            ]
        ]

        return Table(data, colWidths=109, style=DEFAULT_STYLE)

    @staticmethod
    def __calculate_savings_rate(total_income: float, total_savings: float):
        if total_income == 0:
            return 0
        return total_savings / total_income

    @staticmethod
    def __replace_description(description: str) -> str:
        replacements = {
            "APPLE": "Apple",
            "AMZN": "Amazon",
            "AMAZON.DE": "Amazon",
            "Rundfunk": "GEZ",
            "AXA": "Haftpflicht",
            "flaschenpost": "Flaschenpost",
            "AUDIBLE": "Audible",
            "LONDON": "Trip to London",
            "LIEFERANDO": "Lieferando",
            "AUSLANDSENTGELT": "Auslandsendgelt",
            "Takeaway": "Lieferando",
            "DEUTSCHEBAHN": "Deutsche Bahn",
            "DB Vertrieb": "Deutsche Bahn",
            "REWE": "Rewe",
            "HEADSPACE": "Headspace",
            "MONATSGEBÜHR": "American Express",
            "HERR HASE": "Herr Hase",
            "VODAFONE": "Vodafone",
            "MAGNOLIA": "Magnolia",
            "GRAVIS": "Apple",
            "DER GUTE BAECKER": "Krimphove",
            "Miete": "Rent",
            "Kontouebertrag": "Investments",
            "EUROWINGS": "Traveling",
            "BOOKING": "Traveling",
            "American Express Europe": "American Express",
            "AMERICAN EXPRESS EUROPE S.A.": "American Express",
            "ABSCHLAG Strom": "Electricity",
            "ABSCHLAG Gas": "Gas",
            "HALLESCHE": "Private Health Insurance",
            "HOTEL": "Traveling",
            "Universitaet": "Hochschulsport",
            "Bargeldauszahlung": "Cash",
            "Zahnarztpraxis": "Dentist",
            "Sanitaer": "Craftsmans",
            "Galactica": "Going Out",
            "KELLEREI BOZEN": "Trip to Italy",
            "UNTERWEGS": "Cloths",
            "ress- for-less GmbH": "Cloths",
            "E WIE EINFACH": "Electricity",
            "ONEILL": "Cloths",
            "Pension Schmidt": "Pension Smidth",
            "Traix Cycles": "Bycicle",
            "B Vertri eb GmbH": "Deutsche Bahn",
            "DB FERNVERKEHR AG ": "Deutsche Bahn",
            "DM-DROGERIE MARKT": "DM",
            "Drillisch Online GmbH": "Mobile Carrier",
            "CAFE CLASSIQUE": "Café Classique",
            "TOKYO": "Trip to Japan",
            "KYOTO": "Trip to Japan",
            "MINAMITSURU-GUN": "Trip to Japan",
            "BUNBITESBEEF": "Bun Bites Beef",
            "Laufgesellschaft": "Running",
            "CLAUDIA UHLENBROCK": "Barber Shop",
            "X-VIERTEL FRISEUR": "Barber Shop",
            "CINEPLEX": "Cinema",
            "ESSO": "Car",
            "ARAL": "Car",
            "SHELL": "Car",
            "FREIGEIST-MS GMBH": "Gustav Grün",
            "BOHEME BOULETTE": "Bohemé Boulette",
            "SPORT SCHECK": "Running",
            "MUNCHEN": "Trip to München",
            "Haspa Marathon": "Running",
            "Classique": "Café Classique",
            "CLASSIQUE": "Café Classique",
            "CAVETE": "Cavete",
            "Tom + Polly": "Tom + Polly",
            "APOTHEKE": "Apothecary"
        }

        for key, value in replacements.items():
            if key in description:
                return value

        return "Unsorted"
