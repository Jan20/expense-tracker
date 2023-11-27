from flask import jsonify, Blueprint, abort

from application.domain.services.expense_service import ExpenseService
from application.domain.services.kpi_service import KPIService

kpi_service = KPIService()
expense_service = ExpenseService()

kpi_blueprint = Blueprint('kpi', __name__)


@kpi_blueprint.route(rule='/kpi', methods=['GET'])
def get_kpis():
    try:
        kpi = kpi_service.calculate_key_performance_indicators()
        return jsonify({'message': 'Income created successfully', 'expense': kpi.__dict__}), 201

    except ValueError as error:
        abort(404, {'error': str(error)})
