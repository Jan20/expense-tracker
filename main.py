import logging
from flask import Flask

from application.adapters.controllers.expense_controller import expense_blueprint
from application.adapters.controllers.file_controller import file_blueprint
from application.adapters.controllers.income_controller import income_blueprint
from application.adapters.controllers.kpi_controller import kpi_blueprint
from application.adapters.controllers.report_controller import report_blueprint


def create_app() -> Flask:
    app: Flask = Flask(__name__)

    app.register_blueprint(expense_blueprint)
    app.register_blueprint(file_blueprint)
    app.register_blueprint(report_blueprint)
    app.register_blueprint(income_blueprint)
    app.register_blueprint(kpi_blueprint)

    app.logger.setLevel(logging.WARNING)

    return app


if __name__ == '__main__':
    create_app().run(port=5000, debug=True)
