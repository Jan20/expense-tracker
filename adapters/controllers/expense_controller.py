from adapters.persistence.repositories.expense_repository import ExpenseRepository
from flask import Flask, request, jsonify


@app.route('/expenses', methods=['POST'])
def create_expense():
    data = request.json
    user_id = data.get('user_id')
    amount = data.get('amount')
    description = data.get('description')
    currency_code = data.get('currency')

    try:
        expense = ExpenseUser.create_expense(user_id, amount, description, currency_code)
        return jsonify({'message': 'Expense created successfully', 'expense': expense.__dict__}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/expenses/<expense_id>', methods=['GET'])
def get_expense(expense_id):
    try:
        expense = expense_use_case.get_expense(expense_id)
        return jsonify({'expense': expense.__dict__}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@app.route('/expenses/<expense_id>', methods=['PUT'])
def update_expense(expense_id):
    data = request.json
    amount = data.get('amount')
    description = data.get('description')
    currency_code = data.get('currency')

    try:
        expense = expense_use_case.update_expense(expense_id, amount, description, currency_code)
        return jsonify({'message': 'Expense updated successfully', 'expense': expense.__dict__}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@app.route('/expenses/<expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    try:
        expense_use_case.delete_expense(expense_id)
        return jsonify({'message': 'Expense deleted successfully'}), 204
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

if __name__ == '__main__':
    app.run(debug=True)
