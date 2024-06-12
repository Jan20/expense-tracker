import json

from flask import g, request, jsonify, Blueprint, send_file

income_blueprint = Blueprint(name='income', import_name=__name__)


@income_blueprint.route(rule='/income', methods=['POST'])
def generate_financial_report():
    try:
        year: int = json.loads(request.data).get('year')

        if year is None:
            return jsonify({'error': 'Year parameter is missing'}), 400

        g.income_service.create_income_summary(year=year)

        return send_file(path_or_file="files/income_summary.pdf", as_attachment=True)

    except Exception as e:
        return jsonify({'error': str(e)})
