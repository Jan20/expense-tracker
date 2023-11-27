from flask import request, jsonify, Blueprint, abort
from application.domain.services.income_service import IncomeService

income_service = IncomeService()
income_blueprint = Blueprint('income', __name__)


@income_blueprint.route(rule='/incomes', methods=['POST'])
def create_expense():
    data = request.json

    try:
        expense = income_service.create_income(
            date=data.get('timestamp'),
            description=data.get('description'),
            amount=data.get('amount')
        )
        return jsonify({'message': 'Income created successfully', 'expense': expense.__dict__}), 201

    except ValueError as error:
        abort(404, {'error': str(error)})


@income_blueprint.route('/incomes', methods=['GET'])
def get_expenses():
    try:
        incomes = income_service.get_incomes()
        return jsonify({'incomes': incomes}), 200
    except ValueError as error:
        abort(404, {'error': str(error)})


@income_blueprint.route('/incomes/<income_id>', methods=['GET'])
def get_expense(income_id: str):
    try:
        income = income_service.get_income(income_id)
        return jsonify({'expense': income.__dict__}), 200
    except ValueError as error:
        abort(404, {'error': str(error)})


@income_blueprint.route(rule='/incomes/<income_id>', methods=['PUT'])
def update_expense(income_id: str):
    data = request.json

    try:
        income = income_service.update_income(
            income_id=income_id,
            date=data.get('timestamp'),
            description=data.get('description'),
            amount=data.get('amount')
        )
        return jsonify({'message': 'Income updated successfully', 'income': income.__dict__}), 200

    except ValueError as error:
        abort(404, {'error': str(error)})


@income_blueprint.route(rule='/incomes/<income_id>', methods=['DELETE'])
def delete_expense(income_id: str):
    try:
        income_service.delete_income(income_id=income_id)
        return jsonify({'message': 'Income deleted successfully'}), 204
    except ValueError as error:
        abort(404, {'error': str(error)})


@income_blueprint.route(rule='/incomes', methods=['DELETE'])
def delete_expenses():
    try:
        income_service.delete_incomes()
        return jsonify({'message': 'Incomes deleted successfully'}), 204
    except ValueError as error:
        abort(404, {'error': str(error)})
