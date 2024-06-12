import json

from PyPDF2 import PdfMerger
from flask import g, request, jsonify, Blueprint, send_file

report_blueprint = Blueprint(name='report', import_name=__name__)


@report_blueprint.route(rule='/report', methods=['POST'])
def generate_report():
    try:
        year: int = json.loads(request.data).get('year')

        if year is None:
            return jsonify({'error': 'Year parameter is missing'}), 400

        pdf_merger = PdfMerger()

        g.summary_service.create_summary(year=year),
        g.income_service.create_income_summary(year=year),
        g.expense_service.create_expense_summary(year=year),

        for pdf in [
            "./files/summary.pdf",
            "./files/income_summary.pdf",
            "./files/expense_summary.pdf"
        ]:
            pdf_merger.append(pdf)

        with open("files/report.pdf", 'wb') as output_file:
            pdf_merger.write(output_file)
        pdf_merger.close()
        return send_file(path_or_file="files/report.pdf", as_attachment=True)

    except Exception as e:
        return jsonify({'error': str(e)})
