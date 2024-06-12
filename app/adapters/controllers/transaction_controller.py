import json
import logging

from flask import g, Blueprint, request, jsonify, abort, Response

transaction_blueprint = Blueprint('transaction', __name__)


@transaction_blueprint.route(rule='/files', methods=['POST'])
def request_filenames() -> tuple[Response, int] | Response:
    try:
        if request.content_type != 'application/json':
            return jsonify({'error': 'Unsupported Media Type, expected application/json'}), 415

        data = json.loads(request.data)

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        directory = data.get('directory')
        if not directory:
            return jsonify({'error': 'Directory parameter is missing'}), 400

        files = g.import_service.get_files(directory)

        return jsonify({'files': files}), 200

    except FileNotFoundError as e:
        logging.error(f"File not found: {e}")
        return jsonify({'error': 'Directory not found'}), 404

    except ValueError as e:
        logging.error(f"Value error: {e}")
        return jsonify({'error': str(e)}), 400

    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return jsonify({'error': 'An unexpected error occurred'}), 500


@transaction_blueprint.route(rule='/transactions', methods=['POST'])
def import_files():
    try:
        files = json.loads(request.data)
        result = g.import_service.import_transactions_from_files(files)
        return jsonify(result)

    except ValueError as error:
        abort(404, {'error': str(error)})
