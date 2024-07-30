# /app/routes/calls.py
from flask import Blueprint, request, jsonify
from app.models.call import Call
from app.services.call_service import create_call, get_call
from app.utils.validators import validate_call_data
import logging

bp = Blueprint('calls', __name__, url_prefix='/api/calls')


@bp.route('/incoming', methods=['POST'])
def register_incoming_call():
    data = request.json
    if not validate_call_data(data):
        logging.error("Invalid data for incoming call: %s", data)
        return jsonify({'error': 'Invalid data'}), 400

    call = create_call(data, 'incoming')
    logging.info("Incoming call registered: %s", call.to_dict())
    return jsonify(call.to_dict()), 201


@bp.route('/outgoing', methods=['POST'])
def register_outgoing_call():
    data = request.json
    if not validate_call_data(data):
        logging.error("Invalid data for outgoing call: %s", data)
        return jsonify({'error': 'Invalid data'}), 400

    call = create_call(data, 'outgoing')
    logging.info("Outgoing call registered: %s", call.to_dict())
    return jsonify(call.to_dict()), 201


@bp.route('/<int:id>', methods=['GET'])
def get_call_info(id):
    call = get_call(id)
    if call is None:
        logging.warning("Call not found: %d", id)
        return jsonify({'error': 'Call not found'}), 404
    logging.info("Call retrieved: %s", call.to_dict())
    return jsonify(call.to_dict())
