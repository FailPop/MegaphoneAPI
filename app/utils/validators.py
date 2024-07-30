# /app/utils/validators.py
from datetime import datetime
import logging
import re


def validate_call_data(data):
    required_fields = ['phone_number', 'call_time', 'duration']
    if not all(field in data for field in required_fields):
        logging.error("Validation failed: missing fields in %s", data)
        return False

    if not isinstance(data['phone_number'], str) or len(data['phone_number']) < 10:
        logging.error("Validation failed: invalid phone number %s", data['phone_number'])
        return False

    try:
        # Validate using datetime
        datetime.fromisoformat(data['call_time'])
    except ValueError:
        logging.error("Validation failed: invalid call time %s", data['call_time'])
        return False

    if not isinstance(data['duration'], int) or data['duration'] < 0:
        logging.error("Validation failed: invalid duration %s", data['duration'])
        return False

    logging.debug("Validation successful for data: %s", data)
    return True


def validate_phone_data(data):
    """
    Validate phone data.
    Args:
        data (dict): The phone data to validate.
    Returns:
        bool: True if valid, False otherwise.
    """
    required_fields = ['number', 'model', 'owner']
    if not all(field in data for field in required_fields):
        return False

    phone_number = data.get('number')
    if not isinstance(phone_number, str):
        return False

    # Regular expression for validating international phone numbers
    phone_pattern = re.compile(r"^\+?[1-9]\d{1,14}$")
    if not phone_pattern.match(phone_number):
        return False

    return True
