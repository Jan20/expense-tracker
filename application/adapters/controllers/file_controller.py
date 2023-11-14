from flask import Blueprint, request, jsonify
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


@file_blueprint.route(rule='/import-files', methods=['POST'])
def import_files():
    try:
        data = request.get_json()
        directory = data.get('directory')
        return file_service.import_files(directory)

    except Exception as e:
        return jsonify({'error': str(e)})
