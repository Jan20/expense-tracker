import json

from flask import g, request, jsonify, Blueprint, send_file

summary_blueprint = Blueprint(name='summary', import_name=__name__)


@summary_blueprint.route(rule='/summary', methods=['POST'])
def generate_financial_report():
    try:
        year: int = json.loads(request.data).get('year')

        if year is None:
            return jsonify({'error': 'Year parameter is missing'}), 400

        g.summary_service.create_summary(year=year)

        return send_file(path_or_file="files/summary.pdf", as_attachment=True)

    except Exception as e:
        return jsonify({'error': str(e)})
