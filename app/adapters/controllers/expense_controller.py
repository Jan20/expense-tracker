import json

from flask import g, request, jsonify, Blueprint, send_file

expense_blueprint = Blueprint(name='expense', import_name=__name__)


@expense_blueprint.route(rule='/expense', methods=['POST'])
def generate_financial_report():
    try:
        year: int = json.loads(request.data).get('year')

        if year is None:
            return jsonify({'error': 'Year parameter is missing'}), 400

        g.expense_service.create_expense_summary(year=year)

        return send_file(path_or_file="files/expense_summary.pdf", as_attachment=True)

    except Exception as e:
        return jsonify({'error': str(e)})
