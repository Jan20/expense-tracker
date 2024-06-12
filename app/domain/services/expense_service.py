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


class ExpenseService:
    def __init__(self, transaction_service: TransactionService):
        self.transaction_service: TransactionService = transaction_service

    def create_expense_summary(self, year: int) -> SimpleDocTemplate:
        df = self.transaction_service.get_transaction_dataframe(
            year=year,
            transaction_type=TransactionType.EXPENSE
        )
        df = self.__adjust_dataframe(df)

        return SimpleDocTemplate(filename="files/expense_summary.pdf", pagesize=A4).build(
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
        return Paragraph(text=f'Expense Summary {year}', style=ParagraphStyle(
            name='Headline',
            fontSize=24,
            leading=28,
            spaceAfter=12
        ))

    @staticmethod
    def __create_graph(df: DataFrame) -> Image:
        df = df.resample(rule='ME', on='date')['amount'].sum()

        figure = Figure()
        ax = figure.subplots()
        ax.bar(df.index.strftime('%b'), df, align='center', color='#8B0000', label='Expenses')
        ax.set_xlabel('Month')
        ax.set_ylabel('Expenses')
        ax.legend()

        buffer = io.BytesIO()
        figure.savefig(buffer, format="png", dpi=600)
        buffer.seek(0)
        return Image(buffer, width=480, height=360)

    def __adjust_dataframe(self, df: DataFrame) -> DataFrame:
        df['description'] = df['description'].map(self.__replace_description)
        mask = ~df['description'].isin(['American Express', 'Investments'])
        df = df.loc[mask]
        df.loc[:, 'amount'] = -df['amount']
        return df

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
