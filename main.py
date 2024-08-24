from typing import Optional

from fastapi import FastAPI, Body

from pydantic import ValidationError
from models import Base, engine, User, UserRegistrationFilter, UserUpdateFilter, UserNewDataFilter
from queries import init_exchanges, init_debug_tickets, db_get_all_tickets, db_get_filtered_ticket, db_add_new_user, \
    db_get_all_users, db_upd_user, db_get_user

app = FastAPI()
Base.metadata.create_all(engine)
init_exchanges()
init_debug_tickets()


@app.get('/')
def index():
    return {'message': 'Hello, world!'}


@app.get('/api/v1/tickets')
def get_all_tickets():
    return db_get_all_tickets()


@app.get('/api/v1/ticket')
def get_filtered_ticket(coin: Optional[str] = 'USDT', currency: Optional[str] = 'USD',
                        trade_type: Optional[str] = 'BUY'):
    total_data = db_get_filtered_ticket(coin.upper(), currency.upper(), trade_type.upper())
    return total_data


@app.post('/api/v1/user')
def set_new_user(user: UserRegistrationFilter):
    try:
        db_add_new_user(**user.__dict__)
        return {'message': 'Success!', 'user': user}
    except ValidationError as ex:
        return ex.json()


@app.get('/api/v1/users')
def get_all_users():
    return db_get_all_users()


@app.get('/api/v1/user/{user_filter}')
def get_user(user_filter: int):
    return db_get_user(user_filter)


@app.put('/api/v1/user')
def update_user(user_update_filter: UserUpdateFilter, new_data: UserNewDataFilter):
    db_upd_user(user_update_filter, new_data)
    return {'message': 'Success!', 'user': new_data}
