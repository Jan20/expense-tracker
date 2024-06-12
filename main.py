import locale
import logging

from flask import Flask, g

from app.adapters.controllers.expense_controller import expense_blueprint
from app.adapters.controllers.income_controller import income_blueprint
from app.adapters.controllers.report_controller import report_blueprint
from app.adapters.controllers.summary_controller import summary_blueprint
from app.adapters.controllers.transaction_controller import transaction_blueprint
from app.domain.services.expense_service import ExpenseService
from app.domain.services.import_service import ImportService
from app.domain.services.income_service import IncomeService
from app.domain.services.summary_service import SummaryService
from app.domain.services.transaction_service import TransactionService

locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')
locale.setlocale(locale.LC_MONETARY, 'de_DE.UTF-8')


def create_app() -> Flask:
    app: Flask = Flask(__name__)
    app.logger.setLevel(logging.WARNING)
    app = register_blueprints(app)

    @app.before_request
    def before_request() -> None:
        if 'transaction_service' not in g:
            g.transaction_service = TransactionService()

        if 'import_service' not in g:
            g.import_service = ImportService(g.transaction_service)

        if 'income_service' not in g:
            g.income_service = IncomeService(g.transaction_service)

        if 'expense_document_service' not in g:
            g.expense_service = ExpenseService(g.transaction_service)

        if 'summary_document_service' not in g:
            g.summary_service = SummaryService(g.transaction_service)

    return app


def register_blueprints(app: Flask) -> Flask:
    for blueprint in [
        expense_blueprint,
        transaction_blueprint,
        summary_blueprint,
        income_blueprint,
        report_blueprint,
    ]:
        app.register_blueprint(blueprint)

    return app


if __name__ == '__main__':
    create_app().run(host='0.0.0.0', port=5000, debug=True)
