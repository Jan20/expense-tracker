from flask import request, jsonify, Blueprint, abort
from application.domain.services.expense_service import ExpenseService

expense_service = ExpenseService()
expense_blueprint = Blueprint('expenses', __name__)


@expense_blueprint.route(rule='/expenses', methods=['POST'])
def create_expense():
    data = request.json
    timestamp = data.get('timestamp')
    description = data.get('description')
    amount = data.get('amount')

    try:
        expense = expense_service.create_expense(
            date=timestamp,
            description=description,
            amount=amount
        )
        return jsonify({'message': 'Expense created successfully', 'expense': expense.__dict__}), 201

    except ValueError as value_error:
        return jsonify({'error': str(value_error)}), 400


@expense_blueprint.route('/expenses', methods=['GET'])
def get_expenses():
    try:
        expenses = expense_service.get_expenses()
        return jsonify({'expenses': expenses}), 200
    except ValueError as error:
        abort(404, {'error': str(error)})


@expense_blueprint.route('/expenses/<expense_id>', methods=['GET'])
def get_expense(expense_id):
    try:
        expense = expense_service.get_expense(expense_id)
        return jsonify({'expense': expense.__dict__}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404


@expense_blueprint.route(rule='/expenses/<expense_id>', methods=['PUT'])
def update_expense(expense_id):
    data = request.json
    expense_id = expense_id
    timestamp = data.get('timestamp')
    description = data.get('description')
    amount = data.get('amount')

    try:
        expense = expense_service.update_expense(
            expense_id=expense_id,
            date=timestamp,
            description=description,
            amount=amount
        )
        return jsonify({'message': 'Expense updated successfully', 'expense': expense.__dict__}), 200

    except ValueError as e:
        return jsonify({'error': str(e)}), 404


@expense_blueprint.route(rule='/expenses/<expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    try:
        expense_service.delete_expense(expense_id=expense_id)
        return jsonify({'message': 'Expense deleted successfully'}), 204
    except ValueError as e:
        return jsonify({'error': str(e)}), 404


@expense_blueprint.route(rule='/expenses', methods=['DELETE'])
def delete_expenses():
    try:
        expense_service.delete_expenses()
        return jsonify({'message': 'Expense deleted successfully'}), 204
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
