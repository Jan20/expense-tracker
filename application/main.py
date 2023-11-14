from flask import Flask

from application.adapters.controllers.expense_controller import expense_blueprint
from application.adapters.controllers.file_controller import file_blueprint

# Create an instance of the Flask class
app = Flask(__name__)

# Register Blueprints
app.register_blueprint(expense_blueprint)
app.register_blueprint(file_blueprint)

# Run the application
if __name__ == '__main__':
    app.run(port=5000, debug=True)

