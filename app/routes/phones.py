# app/routes/phones.py

from flask import Blueprint, request, jsonify
from app.services.phone_service import create_phone, update_phone, delete_phone, get_phone
from app.utils.validators import validate_phone_data
import logging

bp = Blueprint('phones', __name__, url_prefix='/api/phones')


@bp.route('', methods=['POST'])
def add_phone():
    data = request.json
    if not validate_phone_data(data):
        logging.error("Invalid data for adding phone: %s", data)
        return jsonify({'error': 'Invalid data'}), 400

    phone = create_phone(data)
    logging.info("Phone added: %s", phone.to_dict())
    return jsonify(phone.to_dict()), 201


@bp.route('/<int:id>', methods=['PUT'])
def update_phone_info(id):
    data = request.json
    if not validate_phone_data(data):
        logging.error("Invalid data for updating phone: %s", data)
        return jsonify({'error': 'Invalid data'}), 400

    phone = update_phone(id, data)
    if phone:
        logging.info("Phone updated: %s", phone.to_dict())
        return jsonify(phone.to_dict()), 200
    else:
        logging.warning("Phone not found for update: %d", id)
        return jsonify({'error': 'Phone not found'}), 404


@bp.route('/<int:id>', methods=['DELETE'])
def remove_phone(id):
    result = delete_phone(id)
    if result:
        logging.info("Phone deleted: %d", id)
        return '', 204
    else:
        logging.warning("Phone not found for deletion: %d", id)
        return jsonify({'error': 'Phone not found'}), 404


@bp.route('/<int:id>', methods=['GET'])
def get_phone_info(id):
    phone = get_phone(id)
    if phone:
        logging.info("Phone retrieved: %s", phone.to_dict())
        return jsonify(phone.to_dict()), 200
    else:
        logging.warning("Phone not found: %d", id)
        return jsonify({'error': 'Phone not found'}), 404
