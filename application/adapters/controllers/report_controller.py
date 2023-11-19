from flask import request, jsonify, Blueprint
from application.domain.services.report_service import ReportService

report_blueprint = Blueprint('report', __name__)
report_service = ReportService()


@report_blueprint.route(rule='/report', methods=['POST'])
def generate_financial_report():
    try:
        data = request.json
        year = data.get('year')

        # Validate that 'year' is present in the request
        if year is None:
            return jsonify({'error': 'Year parameter is missing'}), 400

        # Perform some action with the year (e.g., print or process)
        print(f"Received year: {year}")

        report_service.generate_financial_report(year=year)

        # You can customize the response based on your application's needs
        response_message = f"Year {year} received successfully."
        return jsonify({'message': response_message})

    except Exception as e:
        return jsonify({'error': str(e)})
