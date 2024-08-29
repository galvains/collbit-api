import random

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
ENDPOINT = "http://localhost:8000"


def test_home():
    response = client.get(ENDPOINT)
    assert response.status_code == 200
    assert response.json()['status'] == 'success'


def test_can_get_all_tickets():
    payload = {
        "username": "debug",
        "price": 0,
        "orders": 0,
        "available": 0,
        "max_limit": 0,
        "min_limit": 0,
        "rate": 0,
        "pay_methods": {},
        "currency": "usd",
        "coin": "usdt",
        "trade_type": "buy",
        "link": "https://debug.com/",
        "exchange_id": 1
    }
    for _ in range(10):
        add_tickets(payload)

    response = client.get(ENDPOINT + '/api/v1/ticket?username=debug&coin=usdt&currency=usd&trade_type=buy')
    assert response.status_code == 200
    assert len(response.json()['tickets']) == 10


def test_can_get_all_users():
    payload = {
        "telegram_id": random.randint(1, 9999),
        "username": f"debug_{random.randint(1, 9999)}",
        "password": "string",
        "role": "admin"
    }
    add_users(payload)

    response = client.get(ENDPOINT + '/api/v1/users')
    assert response.status_code == 200
    assert len(response.json()['users']) == 1
    assert response.json()['users'][0]['telegram_id'] == payload['telegram_id']


def test_can_add_new_user():
    payload = {
        "telegram_id": random.randint(1, 9999),
        "username": f"debug_{random.randint(1, 9999)}",
        "password": "string",
        "role": "admin"
    }
    user_filter = add_users(payload).json()['user']['id']
    response = client.get(ENDPOINT + f'/api/v1/user/{user_filter}')
    assert response.status_code == 200
    assert response.json()['user']['id'] == user_filter


def test_cat_upd_user():
    add_payload = {
        "telegram_id": random.randint(1, 9999),
        "username": f"debug_{random.randint(1, 9999)}",
        "password": "string",
        "role": "admin"
    }
    user_filter = add_users(add_payload).json()['user']['id']
    add_response = client.get(ENDPOINT + f'/api/v1/user/{user_filter}')
    assert add_response.status_code == 200

    upd_payload = {
        "user_update_filter": {
            "user_id": add_response.json()['user']['id']
        },
        "new_data": {
            "username": f"upd_debug_{random.randint(1, 9999)}",
            "password": "new_string",
            "role": "staff",
            "is_subscriber": True,
            "last_login": "2024-08-28T08:31:11.481Z"
        }
    }

    total_data = upd_user(upd_payload).json()
    updated_user_id = total_data['user']['id']
    update_user_telegram_id = total_data['user']['telegram_id']

    upd_response = client.get(ENDPOINT + f'/api/v1/user/{updated_user_id}')
    assert upd_response.status_code == 200
    assert upd_response.json()['user']['telegram_id'] == update_user_telegram_id


def add_tickets(payload):
    return client.post(ENDPOINT + '/api/v1/ticket', json=payload)


def add_users(payload):
    return client.post(ENDPOINT + '/api/v1/user', json=payload)


def upd_user(payload):
    return client.put(ENDPOINT + '/api/v1/user', json=payload)
