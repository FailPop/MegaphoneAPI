# /tests/test_phones.py
import pytest
from app import create_app, db
from app.models.phone import Phone


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client


def test_add_phone(client):
    response = client.post('/api/phones', json={
        'number': '79031234567',
        'model': 'iPhone 12',
        'owner': 'John Doe'
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['number'] == '79031234567'
    assert data['model'] == 'iPhone 12'
    assert data['owner'] == 'John Doe'


def test_update_phone(client):
    # Сначала добавим телефон
    add_response = client.post('/api/phones', json={
        'number': '79031234567',
        'model': 'iPhone 12',
        'owner': 'John Doe'
    })
    assert add_response.status_code == 201
    phone_data = add_response.get_json()

    # Затем обновим информацию о телефоне
    update_response = client.put(f'/api/phones/{phone_data["id"]}', json={
        'number': '79031234567',
        'model': 'iPhone 13',
        'owner': 'Jane Doe'
    })
    assert update_response.status_code == 200
    updated_data = update_response.get_json()
    assert updated_data['model'] == 'iPhone 13'
    assert updated_data['owner'] == 'Jane Doe'


def test_delete_phone(client):
    # Сначала добавим телефон
    add_response = client.post('/api/phones', json={
        'number': '79031234567',
        'model': 'iPhone 12',
        'owner': 'John Doe'
    })
    assert add_response.status_code == 201
    phone_data = add_response.get_json()

    # Затем удалим телефон
    delete_response = client.delete(f'/api/phones/{phone_data["id"]}')
    assert delete_response.status_code == 204


def test_get_phone_info(client):
    # Сначала добавим телефон
    add_response = client.post('/api/phones', json={
        'number': '79031234567',
        'model': 'iPhone 12',
        'owner': 'John Doe'
    })
    assert add_response.status_code == 201
    phone_data = add_response.get_json()

    # Затем получим информацию о телефоне
    get_response = client.get(f'/api/phones/{phone_data["id"]}')
    assert get_response.status_code == 200
    data = get_response.get_json()
    assert data['number'] == '79031234567'
    assert data['model'] == 'iPhone 12'
    assert data['owner'] == 'John Doe'
