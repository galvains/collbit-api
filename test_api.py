import httpx

from fastapi.testclient import TestClient
from main import app

# client = TestClient(app)
client = httpx.Client()
ENDPOINT = "http://localhost:8000"
tickets_payload = {
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
users_payload = {
    "telegram_id": 100,
    "username": "debug",
    "password": "string",
    "role": "admin"
}
upd_user_payload = {
    "user_update_filter": {
        "user_id": 1
    },
    "new_data": {
        "username": "new_string",
        "password": "new_string",
        "role": "staff",
        "is_subscriber": True,
        "last_login": "2024-08-28T08:31:11.481Z"
    }
}


def test_home():
    response = client.get(ENDPOINT)
    assert response.status_code == 200
    assert response.json() == {'message': 'Hello, world!'}


def test_can_get_all_tickets():
    for _ in range(10):
        add_tickets()

    response = client.get(ENDPOINT + '/api/v1/ticket?username=debug&coin=usdt&currency=usd&trade_type=buy')
    assert response.status_code == 200
    assert len(response.json()) == 10


def test_can_add_new_user():
    user_filter = add_users().json()['user']['id']
    response = client.get(ENDPOINT + f'/api/v1/user/{user_filter}')
    assert response.status_code == 200
    assert response.json()['id'] == user_filter


def test_cat_upd_user():
    total_data = upd_user().json()
    updated_user_id = total_data['user']['id']
    update_user_username = total_data['user']['username']

    response = client.get(ENDPOINT + f'/api/v1/user/{updated_user_id}')
    assert response.status_code == 200
    assert response.json()['username'] == update_user_username


def test_can_get_all_users():
    response = client.get(ENDPOINT + '/api/v1/users')
    assert response.status_code == 200
    assert len(response.json()) == 1


def add_tickets():
    return client.post(ENDPOINT + '/api/v1/ticket', json=tickets_payload)


def add_users():
    return client.post(ENDPOINT + '/api/v1/user', json=users_payload)


def upd_user():
    return client.put(ENDPOINT + '/api/v1/user', json=upd_user_payload)
