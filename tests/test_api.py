import os
import random
import httpx

from dotenv import load_dotenv

load_dotenv()
ADMIN_TELEGRAM_ID = int(os.getenv("ADMIN_TELEGRAM_ID"))
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

client = httpx.Client()
ENDPOINT = "http://localhost:8000"


def test_home():
    response = client.get(ENDPOINT)
    assert response.status_code == 200
    assert response.json()['status'] == 'success'


def test_can_login_as_admin():
    auth_logout()

    admin_payload = {
        "telegram_id": ADMIN_TELEGRAM_ID,
        "password": ADMIN_PASSWORD
    }
    auth_admin(admin_payload)

    response = client.get(ENDPOINT + "/auth/me")
    check_role = response.json()['role']
    assert response.status_code == 200
    assert check_role == 'admin'


def test_can_add_new_user():
    payload = {
        "telegram_id": random.randint(1, 9999),
        "username": f"debug_{random.randint(1, 9999)}",
        "password": "string",
        "role": "admin",
        "subscription_id": None
    }
    user_filter = add_users(payload).json()['user']['id']
    response = client.get(ENDPOINT + f'/api/v1/user/{user_filter}')
    assert response.status_code == 200
    assert response.json()['user']['id'] == user_filter


def test_can_add_new_subscription():
    user_payload = {
        "telegram_id": random.randint(1, 9999),
        "username": f"debug_{random.randint(1, 9999)}",
        "password": "string",
        "role": "admin",
        "subscription_id": None
    }

    user_filter = add_users(user_payload).json()['user']['id']
    user_response = client.get(ENDPOINT + f'/api/v1/user/{user_filter}')
    assert user_response.status_code == 200

    sub_payload = {
        "user_id": user_response.json()['user']['id'],
        "subscription_type": "hard",
        "end_date": "2030-01-01T00:00:00.000Z"
    }

    subscriptions_filter = add_subscriptions(sub_payload).json()['subscription']['id']
    sub_response = client.get(ENDPOINT + f'/api/v1/subscription/{subscriptions_filter}')
    assert sub_response.status_code == 200
    assert sub_response.json()['subscription']['id'] == subscriptions_filter

    user_response = client.get(ENDPOINT + f'/api/v1/user/{user_filter}')
    assert user_response.status_code == 200
    assert user_response.json()['user']['subscription_id'] == subscriptions_filter


def test_can_add_new_exchange():
    payload = {
        "name": f"debug_{random.randint(1, 9999)}",
    }
    exchange_filter = add_exchanges(payload).json()['exchange']['id']
    response = client.get(ENDPOINT + f'/api/v1/exchange/{exchange_filter}')

    assert response.status_code == 200
    assert response.json()['exchange']['id'] == exchange_filter


def test_can_add_new_ticket():
    del_all_tickets()
    payload = {
        "username": "debug",
        "price": 0,
        "orders": 0,
        "available": 0,
        "max_limit": 0,
        "min_limit": 0,
        "rate": 0,
        "pay_methods": {},
        "currency": "eur",
        "coin": "usdc",
        "trade_type": "sell",
        "link": "https://debug.com/",
        "exchange_id": 1
    }
    ticket_filter = add_tickets(payload).json()['ticket_id']
    response = client.get(ENDPOINT + '/api/v1/ticket?username=debug&coin=usdc&currency=eur&trade_type=sell')

    assert response.status_code == 200
    assert response.json()['tickets'][0]['id'] == ticket_filter


def test_can_upd_user():
    add_payload = {
        "telegram_id": random.randint(1, 9999),
        "username": f"debug_{random.randint(1, 9999)}",
        "password": "string",
        "role": "admin",
        "subscription_id": None
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
            "last_login": "2024-08-28T08:31:11.481Z",
            "subscription_id": None

        }
    }

    total_data = upd_user(upd_payload).json()
    updated_user_id = total_data['user']['id']
    update_user_telegram_id = total_data['user']['telegram_id']

    upd_response = client.get(ENDPOINT + f'/api/v1/user/{updated_user_id}')
    assert upd_response.status_code == 200
    assert upd_response.json()['user']['telegram_id'] == update_user_telegram_id


def test_can_upd_subscription():
    user_payload = {
        "telegram_id": random.randint(1, 9999),
        "username": f"debug_{random.randint(1, 9999)}",
        "password": "string",
        "role": "admin",
        "subscription_id": None
    }

    user_filter = add_users(user_payload).json()['user']['id']
    user_response = client.get(ENDPOINT + f'/api/v1/user/{user_filter}')
    assert user_response.status_code == 200

    sub_payload = {
        "user_id": user_response.json()['user']['id'],
        "subscription_type": "hard",
        "end_date": "2030-01-01T00:00:00.000Z"
    }

    subscriptions_filter = add_subscriptions(sub_payload).json()['subscription']['id']
    sub_response = client.get(ENDPOINT + f'/api/v1/subscription/{subscriptions_filter}')
    assert sub_response.status_code == 200
    assert sub_response.json()['subscription']['id'] == subscriptions_filter

    upd_sub_payload = {
        "subscription_update_filter": {
            "subscription_id": subscriptions_filter
        },
        "new_data": {
            "subscription_type": "medium",
            "start_date": "2000-01-01T00:00:00.000Z",
            "end_date": "2030-01-01T00:00:00.000Z"
        }
    }

    total_upd_sub = upd_subscription(upd_sub_payload).json()
    upd_sub_filter = total_upd_sub['subscription']['id']
    upd_sub_type = total_upd_sub['subscription']['subscription_type']

    sub_response = client.get(ENDPOINT + f'/api/v1/subscription/{subscriptions_filter}')
    assert sub_response.status_code == 200
    assert sub_response.json()['subscription']['id'] == upd_sub_filter
    assert sub_response.json()['subscription']['subscription_type'] == upd_sub_type


def test_can_upd_exchange():
    payload = {
        "name": f"debug_{random.randint(1, 9999)}",
    }
    exchange_filter = add_exchanges(payload).json()['exchange']['id']
    response = client.get(ENDPOINT + f'/api/v1/exchange/{exchange_filter}')

    assert response.status_code == 200
    assert response.json()['exchange']['id'] == exchange_filter

    upd_payload = {
        "exchange_update_filter": {
            "exchange_id": 4
        },
        "new_data": {
            "name": "new_data_name"
        }
    }

    upd_exchange_filter = upd_exchange(upd_payload).json()['exchange']['id']
    upd_response = client.get(ENDPOINT + f'/api/v1/exchange/{upd_exchange_filter}')
    assert upd_response.status_code == 200
    assert upd_response.json()['exchange']['name'] == upd_payload['new_data']['name']


def test_can_get_all_tickets():
    del_all_tickets()
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


def test_can_get_user():
    user_payload = {
        "telegram_id": random.randint(1, 9999),
        "username": f"debug_{random.randint(1, 9999)}",
        "password": "string",
        "role": "admin",
        "subscription_id": None
    }
    add_users(user_payload)

    user_filter = None
    response = client.get(ENDPOINT + '/api/v1/users')
    for user in response.json()['users']:
        if user['telegram_id'] == user_payload['telegram_id']:
            user_filter = user['id']

    response = client.get(ENDPOINT + f'/api/v1/user/{user_filter}')
    assert response.status_code == 200
    assert response.json()['user']['id'] == user_filter


def test_can_get_ticket():
    payload = {
        "username": "debug",
        "price": 0,
        "orders": 0,
        "available": 0,
        "max_limit": 0,
        "min_limit": 0,
        "rate": 0,
        "pay_methods": {},
        "currency": "eur",
        "coin": "usdc",
        "trade_type": "sell",
        "link": "https://debug.com/",
        "exchange_id": 1
    }
    ticket_filter = add_tickets(payload).json()['ticket_id']
    response = client.get(ENDPOINT + '/api/v1/ticket?username=debug&coin=usdc&currency=eur&trade_type=sell')

    assert response.status_code == 200
    assert response.json()['tickets'][0]['id'] == ticket_filter


def test_can_get_exchange():
    payload = {
        "name": f"debug_{random.randint(1, 9999)}",
    }
    exchange_filter = add_exchanges(payload).json()['exchange']['id']
    response = client.get(ENDPOINT + f'/api/v1/exchange/{exchange_filter}')

    assert response.status_code == 200
    assert response.json()['exchange']['id'] == exchange_filter


def test_can_get_subscription():
    user_payload = {
        "telegram_id": random.randint(1, 9999),
        "username": f"debug_{random.randint(1, 9999)}",
        "password": "string",
        "role": "admin",
        "subscription_id": None
    }

    user_filter = add_users(user_payload).json()['user']['id']
    user_response = client.get(ENDPOINT + f'/api/v1/user/{user_filter}')
    assert user_response.status_code == 200

    sub_payload = {
        "user_id": user_response.json()['user']['id'],
        "subscription_type": "hard",
        "end_date": "2030-01-01T00:00:00.000Z"
    }

    subscriptions_filter = add_subscriptions(sub_payload).json()['subscription']['id']
    sub_response = client.get(ENDPOINT + f'/api/v1/subscription/{subscriptions_filter}')
    assert sub_response.status_code == 200
    assert sub_response.json()['subscription']['id'] == subscriptions_filter

    user_response = client.get(ENDPOINT + f'/api/v1/user/{user_filter}')
    assert user_response.status_code == 200
    assert user_response.json()['user']['subscription_id'] == subscriptions_filter


def test_can_del_user():
    add_payload = {
        "telegram_id": random.randint(1, 9999),
        "username": f"debug_{random.randint(1, 9999)}",
        "password": "string",
        "role": "admin"
    }
    user_filter = add_users(add_payload).json()['user']['id']
    add_response = client.get(ENDPOINT + f'/api/v1/user/{user_filter}')
    assert add_response.status_code == 200

    del_user(user_filter)

    del_response = client.get(ENDPOINT + f'/api/v1/user/{user_filter}')
    assert del_response.status_code == 404


def test_can_del_ticket():
    add_payload = {
        "username": f"debug_{random.randint(1, 9999)}",
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

    add_tickets(add_payload)

    add_response = client.get(
        ENDPOINT + f"/api/v1/ticket?username={add_payload['username']}&coin=usdt&currency=usd&trade_type=buy")
    assert add_response.status_code == 200
    del_ticket(add_response.json()['tickets'][0]['id'])

    del_response = client.get(
        ENDPOINT + f"/api/v1/ticket?username={add_payload['username']}&coin=usdt&currency=usd&trade_type=buy")
    assert del_response.status_code == 404


def test_can_del_subscription():
    user_payload = {
        "telegram_id": random.randint(1, 9999),
        "username": f"debug_{random.randint(1, 9999)}",
        "password": "string",
        "role": "admin",
        "subscription_id": None
    }

    user_filter = add_users(user_payload).json()['user']['id']
    user_response = client.get(ENDPOINT + f'/api/v1/user/{user_filter}')
    assert user_response.status_code == 200

    sub_payload = {
        "user_id": user_response.json()['user']['id'],
        "subscription_type": "hard",
        "end_date": "2030-01-01T00:00:00.000Z"
    }

    subscriptions_filter = add_subscriptions(sub_payload).json()['subscription']['id']
    sub_response = client.get(ENDPOINT + f'/api/v1/subscription/{subscriptions_filter}')
    assert sub_response.status_code == 200
    assert sub_response.json()['subscription']['id'] == subscriptions_filter

    user_response = client.get(ENDPOINT + f'/api/v1/user/{user_filter}')
    assert user_response.status_code == 200
    assert user_response.json()['user']['subscription_id'] == subscriptions_filter

    del_subscription(subscriptions_filter)
    sub_response = client.get(ENDPOINT + f'/api/v1/subscription/{subscriptions_filter}')
    assert sub_response.status_code == 404


def test_can_del_exchange():
    payload = {
        "name": f"debug_{random.randint(1, 9999)}",
    }
    exchange_filter = add_exchanges(payload).json()['exchange']['id']
    response = client.get(ENDPOINT + f'/api/v1/exchange/{exchange_filter}')

    assert response.status_code == 200
    assert response.json()['exchange']['id'] == exchange_filter

    del_exchange(exchange_filter)
    response = client.get(ENDPOINT + f'/api/v1/exchange/{exchange_filter}')
    assert response.status_code == 404


def test_can_del_all_tickets():
    del_all_tickets()

    response = client.get(ENDPOINT + f'/api/v1/tickets')
    assert response.status_code == 404


# def test_can_del_all_users():
#     del_all_users()
#
#     response = client.get(ENDPOINT + f'/api/v1/users')
#     assert response.status_code == 404


def add_tickets(payload):
    return client.post(ENDPOINT + '/api/v1/ticket', json=payload)


def add_users(payload):
    return client.post(ENDPOINT + '/auth/register', json=payload)


def add_subscriptions(payload):
    return client.post(ENDPOINT + '/api/v1/subscription', json=payload)


def add_exchanges(payload):
    return client.post(ENDPOINT + '/api/v1/exchange', json=payload)


def upd_user(payload):
    return client.put(ENDPOINT + '/api/v1/user', json=payload)


def upd_subscription(payload):
    return client.put(ENDPOINT + '/api/v1/subscription', json=payload)


def upd_exchange(payload):
    return client.put(ENDPOINT + '/api/v1/exchange', json=payload)


def del_user(user_id):
    return client.delete(ENDPOINT + f'/api/v1/user/{user_id}')


def del_ticket(ticket_id):
    return client.delete(ENDPOINT + f'/api/v1/ticket/{ticket_id}')


def del_subscription(subscription_id):
    return client.delete(ENDPOINT + f'/api/v1/subscription/{subscription_id}')


def del_exchange(exchange_id):
    return client.delete(ENDPOINT + f'/api/v1/exchange/{exchange_id}')


# def del_all_users():
#     return client.delete(ENDPOINT + '/api/v1/users')


def del_all_tickets():
    return client.delete(ENDPOINT + '/api/v1/tickets')


def auth_admin(payload):
    return client.post(ENDPOINT + '/auth/login', json=payload)


def auth_logout():
    return client.post(ENDPOINT + "/auth/logout")
