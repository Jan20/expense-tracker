from flask import Blueprint, request, jsonify, abort, Response
from application.domain.services.file_service import FileService


file_blueprint = Blueprint('file', __name__)
file_service = FileService()


@file_blueprint.route(rule='/files', methods=['GET'])
def get_filenames():
    try:
        data = request.get_json()
        directory = data.get('directory')
        return file_service.get_files(directory)

    except Exception as e:
        return jsonify({'error': str(e)})


@file_blueprint.route(rule='/files', methods=['POST'])
def import_files():
    try:
        data = request.get_json()
        directory: str = data.get('directory')
        transaction_type: str = data.get('transaction_type')

        if transaction_type == "income":
            result = file_service.import_incomes_from_file(directory)
        elif transaction_type == "expenses":
            result = file_service.import_expenses_from_file(directory)
        else:
            abort(400, 'Expects either income or expense')

        return jsonify(result)

    except ValueError as error:
        abort(404, {'error': str(error)})
