# /app/services/call_service.py
from app import db
from app.models.call import Call
import logging
import requests
import os

MEGAFON_API_BASE_URL = "https://api.megafon.ru/v1"
MEGAFON_API_KEY = os.environ.get('MEGAFON_API_KEY')

def create_call(data, call_type):
    call = Call(
        phone_number=data['phone_number'],
        call_time=data['call_time'],
        duration=data['duration'],
        type=call_type
    )
    db.session.add(call)
    db.session.commit()
    logging.debug("Call created: %s", call.to_dict())
    return call

def get_call(call_id):
    call = Call.query.get(call_id)
    if call:
        logging.debug("Call found: %s", call.to_dict())
    else:
        logging.debug("Call not found: %d", call_id)
    return call

def start_call_record(call_id):
    call = get_call(call_id)
    if not call:
        logging.error("Call not found for call_id: %d", call_id)
        return None

    url = f"{MEGAFON_API_BASE_URL}/calls/{call_id}/record/start"
    headers = {
        "Authorization": f"Bearer {MEGAFON_API_KEY}".encode('utf-8'),
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers)

    if response.status_code == 200:
        logging.debug("Call record started for call_id: %d", call_id)
        return response.json()
    else:
        logging.error("Failed to start call record for call_id: %d", call_id)
        return None

def stop_call_record(record_id):
    url = f"{MEGAFON_API_BASE_URL}/records/{record_id}/stop"
    headers = {
        "Authorization": f"Bearer {MEGAFON_API_KEY}".encode('utf-8'),
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers)

    if response.status_code == 200:
        logging.debug("Call record stopped for record_id: %d", record_id)
        return response.json()
    else:
        logging.error("Failed to stop call record for record_id: %d", record_id)
        return None

def get_call_record(record_id):
    url = f"{MEGAFON_API_BASE_URL}/records/{record_id}"
    headers = {
        "Authorization": f"Bearer {MEGAFON_API_KEY}".encode('utf-8'),
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        logging.debug("Call record retrieved for record_id: %d", record_id)
        return response.json()
    else:
        logging.error("Failed to retrieve call record for record_id: %d", record_id)
        return None
