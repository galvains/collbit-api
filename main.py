from typing import Optional

from fastapi import FastAPI

from pydantic import ValidationError
from models import Base, engine, User, UserRegistrationFilter, UserUpdateFilter, UserNewDataFilter, TicketCreateFilter
from queries import init_exchanges, init_debug_tickets, db_get_all_tickets, db_get_filtered_ticket, db_add_new_user, \
    db_get_all_users, db_upd_user, db_get_user, db_add_new_ticket

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
def get_filtered_ticket(coin: Optional[str] = 'usdt', currency: Optional[str] = 'usd',
                        trade_type: Optional[str] = 'sell'):
    total_data = db_get_filtered_ticket(coin, currency, trade_type)
    return total_data


@app.post('/api/v1/ticket')
def set_new_ticket(ticket: TicketCreateFilter):
    try:
        db_add_new_ticket(**ticket.__dict__)
        return {'message': 'Success!', 'ticket': ticket}
    except ValidationError as ex:
        return ex.json()


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
