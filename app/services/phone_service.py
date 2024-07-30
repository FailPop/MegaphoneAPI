# /app/services/phone_service.py
from app import db
from app.models.phone import Phone
import logging

def create_phone(data):
    phone = Phone(
        number=data['number'],
        model=data['model'],
        owner=data['owner']
    )
    db.session.add(phone)
    db.session.commit()
    logging.debug("Phone created: %s", phone.to_dict())
    return phone

def update_phone(phone_id, data):
    phone = Phone.query.get(phone_id)
    if phone:
        phone.number = data.get('number', phone.number)
        phone.model = data.get('model', phone.model)
        phone.owner = data.get('owner', phone.owner)
        db.session.commit()
        logging.debug("Phone updated: %s", phone.to_dict())
        return phone
    logging.debug("Phone not found for update: %d", phone_id)
    return None

def delete_phone(phone_id):
    phone = Phone.query.get(phone_id)
    if phone:
        db.session.delete(phone)
        db.session.commit()
        logging.debug("Phone deleted: %d", phone_id)
        return True
    logging.debug("Phone not found for deletion: %d", phone_id)
    return False

def get_phone(phone_id):
    phone = Phone.query.get(phone_id)
    if phone:
        logging.debug("Phone found: %s", phone.to_dict())
    else:
        logging.debug("Phone not found: %d", phone_id)
    return phone