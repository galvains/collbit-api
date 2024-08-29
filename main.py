from fastapi import FastAPI, Depends, HTTPException

from pydantic import ValidationError
from models import Base, engine, UserRegistrationFilter, UserUpdateFilter, UserNewDataFilter, TicketCreateFilter, \
    GetTicketFilter, TicketDeleteFilter

from queries import init_exchanges, init_debug_tickets, db_get_all_tickets, db_get_filtered_ticket, db_add_new_user, \
    db_get_all_users, db_upd_user, db_get_user, db_add_new_ticket, db_del_ticket

app = FastAPI()
Base.metadata.create_all(engine)
init_exchanges()
init_debug_tickets()


@app.get('/')
def index():
    return {"status": "success", 'message': 'Hello, world!'}


@app.get('/api/v1/tickets')
def get_all_tickets():
    tickets = db_get_all_tickets()
    if tickets:
        return {"status": "success", 'tickets': tickets}
    else:
        raise HTTPException(status_code=404, detail='Tickets not found')


@app.post('/api/v1/ticket')
def set_new_ticket(ticket: TicketCreateFilter):
    new_ticket = db_add_new_ticket(**ticket.__dict__)
    if new_ticket:
        return {"status": "success", 'ticket_id': new_ticket}
    else:
        raise HTTPException(status_code=404, detail='Error added ticket')


@app.post('/api/v1/user')
def set_new_user(user: UserRegistrationFilter):
    new_user = db_add_new_user(**user.__dict__)
    if new_user:
        return {"status": "success", 'user': new_user}
    else:
        raise HTTPException(status_code=400, detail='User already exists')


@app.get('/api/v1/users')
def get_all_users():
    users = db_get_all_users()
    if users:
        return {"status": "success", 'users': users}
    else:
        raise HTTPException(status_code=404, detail='Users not found')


@app.get('/api/v1/user/{user_id}')
def get_user(user_id: int):
    user = db_get_user(user_id)
    if user:
        return {"status": "success", 'user': user}
    else:
        raise HTTPException(status_code=404, detail='User not found')


@app.put('/api/v1/user')
def update_user(user_update_filter: UserUpdateFilter, new_data: UserNewDataFilter):
    updater_user = db_upd_user(user_update_filter, new_data)
    if updater_user:
        return {"status": "success", 'user': updater_user}
    else:
        raise HTTPException(status_code=400, detail='User not found')


@app.get('/api/v1/ticket')
def get_filtered_ticket(filter_ticket: GetTicketFilter = Depends()):
    tickets = db_get_filtered_ticket(**filter_ticket.__dict__)
    if tickets:
        return {"status": "success", 'tickets': tickets}
    else:
        raise HTTPException(status_code=400, detail='Tickets not found')


@app.delete('/api/v1/ticket')
def delete_ticket(ticket: TicketDeleteFilter):
    delete = db_del_ticket(ticket.key, ticket.value)
    if delete:
        return {"status": "success"}
    else:
        raise HTTPException(status_code=400, detail="Error deleting ticket")
