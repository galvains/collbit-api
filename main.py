from typing import Optional

from fastapi import FastAPI, Depends

from pydantic import ValidationError
from models import Base, engine, User, UserRegistrationFilter, UserUpdateFilter, UserNewDataFilter, TicketCreateFilter, \
    GetTicketFilter

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
        result = db_add_new_user(**user.__dict__)
        return {'message': 'Success!', 'user': result}
    except ValidationError as ex:
        return ex.json()


@app.get('/api/v1/users')
def get_all_users():
    return db_get_all_users()


@app.get('/api/v1/user/{user_id}')
def get_user(user_id: int):
    return db_get_user(user_id)


@app.put('/api/v1/user')
def update_user(user_update_filter: UserUpdateFilter, new_data: UserNewDataFilter):
    result = db_upd_user(user_update_filter, new_data)
    return {'message': 'Success!', 'user': result}


@app.get('/api/v1/ticket')
def get_filtered_ticket(filter_ticket: GetTicketFilter = Depends()):
    return db_get_filtered_ticket(**filter_ticket.__dict__)

