# /app/routes/call_records.py
from flask import Blueprint, request, jsonify
from app.services.call_service import start_call_record, stop_call_record, get_call_record
import logging

bp = Blueprint('call_records', __name__, url_prefix='/api/call-records')

@bp.route('/start', methods=['POST'])
def start_record():
    data = request.json
    if 'call_id' not in data:
        logging.error("Invalid data for starting call record: %s", data)
        return jsonify({'error': 'Invalid data'}), 400

    record = start_call_record(data['call_id'])
    if record:
        logging.info("Call record started: %s", record)
        return jsonify(record), 201
    else:
        logging.error("Failed to start call record for call_id: %s", data['call_id'])
        return jsonify({'error': 'Failed to start call record'}), 500

@bp.route('/stop', methods=['POST'])
def stop_record():
    data = request.json
    if 'record_id' not in data:
        logging.error("Invalid data for stopping call record: %s", data)
        return jsonify({'error': 'Invalid data'}), 400

    record = stop_call_record(data['record_id'])
    if record:
        logging.info("Call record stopped: %s", record)
        return jsonify(record), 200
    else:
        logging.error("Failed to stop call record for record_id: %s", data['record_id'])
        return jsonify({'error': 'Failed to stop call record'}), 500

@bp.route('/<int:id>', methods=['GET'])
def get_record(id):
    record = get_call_record(id)
    if record:
        logging.info("Call record retrieved: %s", record)
        return jsonify(record), 200
    else:
        logging.warning("Call record not found: %d", id)
        return jsonify({'error': 'Call record not found'}), 404