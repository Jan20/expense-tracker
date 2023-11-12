from datetime import datetime

from application.adapters.persistence.repositories.expense_repository import ExpenseRepository
from flask import Flask, request, jsonify

from application.services.expense_service import ExpenseService

# Create an instance of the Flask class
app = Flask(__name__)

expense_repository = ExpenseRepository()
expense_service = ExpenseService(expense_repository)


@app.route(rule='/expenses', methods=['POST'])
def create_expense():
    data = request.json
    timestamp = data.get('timestamp')
    description = data.get('description')
    amount = data.get('amount')

    timestamp = datetime.now()

    try:
        expense = expense_service.create_expense(
            timestamp=timestamp,
            description=description,
            amount=amount
        )
        return jsonify({'message': 'Expense created successfully', 'expense': expense.__dict__}), 201

    except ValueError as value_error:
        return jsonify({'error': str(value_error)}), 400


@app.route('/expenses', methods=['GET'])
def get_expenses():
    try:
        expenses = expense_service.get_expenses()
        print(expenses)
        return jsonify({'expenses': expenses}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404


@app.route('/expenses/<expense_id>', methods=['GET'])
def get_expense(expense_id):
    try:
        expense = expense_service.get_expense(expense_id)
        return jsonify({'expense': expense.__dict__}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404


@app.route(rule='/expenses/<expense_id>', methods=['PUT'])
def update_expense(expense_id):
    data = request.json
    expense_id = expense_id
    timestamp = data.get('timestamp')
    description = data.get('description')
    amount = data.get('amount')

    try:
        expense = expense_service.update_expense(
            expense_id=expense_id,
            timestamp=timestamp,
            description=description,
            amount=amount
        )
        return jsonify({'message': 'Expense updated successfully', 'expense': expense.__dict__}), 200

    except ValueError as e:
        return jsonify({'error': str(e)}), 404


@app.route(rule='/expenses/<expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    try:
        expense_service.delete_expense(expense_id=expense_id)
        return jsonify({'message': 'Expense deleted successfully'}), 204
    except ValueError as e:
        return jsonify({'error': str(e)}), 404


if __name__ == '__main__':
    app.run(debug=True)
