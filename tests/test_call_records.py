# /tests/test_call_records.py
import pytest
from app import create_app, db
from app.models.call import Call
import os

TEST_PHONE_NUMBER = os.environ.get('TEST_PHONE_NUMBER')


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client


def test_start_call_record(client):
    # Сначала зарегистрируем звонок
    call_response = client.post('/api/calls/incoming', json={
        'phone_number': TEST_PHONE_NUMBER,
        'call_time': '2024-07-25T14:30:00',
        'duration': 120
    })
    assert call_response.status_code == 201
    call_data = call_response.get_json()

    # Затем начнем запись звонка
    record_response = client.post('/api/call-records/start', json={
        'call_id': call_data['id']
    })
    assert record_response.status_code == 201
    record_data = record_response.get_json()
    assert 'message' in record_data


def test_stop_call_record(client):
    # Сначала зарегистрируем звонок
    call_response = client.post('/api/calls/incoming', json={
        'phone_number': TEST_PHONE_NUMBER,
        'call_time': '2024-07-25T14:30:00',
        'duration': 120
    })
    assert call_response.status_code == 201
    call_data = call_response.get_json()

    # Затем начнем запись звонка
    start_response = client.post('/api/call-records/start', json={
        'call_id': call_data['id']
    })
    assert start_response.status_code == 201
    start_data = start_response.get_json()

    # И наконец остановим запись звонка
    stop_response = client.post('/api/call-records/stop', json={
        'record_id': start_data['record_id']
    })
    assert stop_response.status_code == 200
    stop_data = stop_response.get_json()
    assert 'message' in stop_data


def test_get_call_record(client):
    # Сначала зарегистрируем звонок
    call_response = client.post('/api/calls/incoming', json={
        'phone_number': TEST_PHONE_NUMBER,
        'call_time': '2024-07-25T14:30:00',
        'duration': 120
    })
    assert call_response.status_code == 201
    call_data = call_response.get_json()

    # Затем начнем запись звонка
    start_response = client.post('/api/call-records/start', json={
        'call_id': call_data['id']
    })
    assert start_response.status_code == 201
    start_data = start_response.get_json()

    # Получим запись звонка
    record_response = client.get(f'/api/call-records/{start_data["record_id"]}')
    assert record_response.status_code == 200
    record_data = record_response.get_json()
    assert 'message' in record_data
