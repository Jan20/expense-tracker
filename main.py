from flask import Flask

from application.adapters.controllers.expense_controller import expense_blueprint
from application.adapters.controllers.file_controller import file_blueprint
from application.adapters.controllers.report_controller import report_blueprint


def create_app() -> Flask:
    # Create an instance of the Flask class
    app: Flask = Flask(__name__)

    # Register Blueprints
    app.register_blueprint(expense_blueprint)
    app.register_blueprint(file_blueprint)
    app.register_blueprint(report_blueprint)

    return app


if __name__ == '__main__':
    create_app().run(port=5000, debug=True)
