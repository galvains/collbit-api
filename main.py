import asyncio

from fastapi import FastAPI, Depends, HTTPException
from contextlib import asynccontextmanager

from app.models import Base, engine, UserRegistrationFilter, UserUpdateFilter, UserNewDataFilter, TicketCreateFilter, \
    GetTicketFilter

from app.queries import init_exchanges, init_debug_tickets, db_get_all_tickets, db_get_filtered_ticket, db_add_new_user, \
    db_get_all_users, db_upd_user, db_get_user, db_add_new_ticket, db_del_ticket, db_del_user, db_del_all_users, \
    db_del_all_tickets


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await init_exchanges()
    await init_debug_tickets()

    yield


app = FastAPI(lifespan=lifespan)


@app.get('/')
async def index():
    return {"status": "success", 'message': 'Hello, world!'}


@app.get('/api/v1/tickets', summary="Get all tickets")
async def get_all_tickets():
    tickets = await db_get_all_tickets()
    if tickets:
        return {"status": "success", 'tickets': tickets}
    else:
        raise HTTPException(status_code=404, detail='Tickets not found')


@app.post('/api/v1/ticket', summary="Set new ticket")
async def set_new_ticket(ticket: TicketCreateFilter):
    new_ticket = await db_add_new_ticket(**ticket.__dict__)
    if new_ticket:
        return {"status": "success", 'ticket_id': new_ticket}
    else:
        raise HTTPException(status_code=404, detail='Error added ticket')


@app.post('/api/v1/user', summary="Set new user")
async def set_new_user(user: UserRegistrationFilter):
    new_user = await db_add_new_user(**user.__dict__)
    if new_user:
        return {"status": "success", 'user': new_user}
    else:
        raise HTTPException(status_code=400, detail='User already exists')


@app.get('/api/v1/users', summary="Get all users")
async def get_all_users():
    users = await db_get_all_users()
    if users:
        return {"status": "success", 'users': users}
    else:
        raise HTTPException(status_code=404, detail='Users not found')


@app.get('/api/v1/user/{user_id}', summary="Get a filtered user")
async def get_user(user_id: int):
    user = await db_get_user(user_id)
    if user:
        return {"status": "success", 'user': user}
    else:
        raise HTTPException(status_code=404, detail='User not found')


@app.put('/api/v1/user', summary="Update a user")
async def update_user(user_update_filter: UserUpdateFilter, new_data: UserNewDataFilter):
    updater_user = await db_upd_user(user_update_filter, new_data)
    if updater_user:
        return {"status": "success", 'user': updater_user}
    else:
        raise HTTPException(status_code=404, detail='User not found')


@app.get('/api/v1/ticket', summary="Get a filtered ticket")
async def get_filtered_ticket(filter_ticket: GetTicketFilter = Depends()):
    tickets = await db_get_filtered_ticket(**filter_ticket.__dict__)
    if tickets:
        return {"status": "success", 'tickets': tickets}
    else:
        raise HTTPException(status_code=404, detail='Tickets not found')


@app.delete('/api/v1/ticket/{ticket_id}', summary="Delete a ticket")
async def delete_ticket(ticket_id: int):
    delete = await db_del_ticket(ticket_id)
    if delete:
        return {"status": "success"}
    else:
        raise HTTPException(status_code=400, detail="Error deleting ticket")


@app.delete('/api/v1/user/{user_id}', summary="Delete a user")
async def delete_user(user_id: int):
    delete = await db_del_user(user_id)
    if delete:
        return {"status": "success"}
    else:
        raise HTTPException(status_code=400, detail="Error deleting user")


@app.delete('/api/v1/users', summary="Delete all users")
async def delete_all_users():
    delete_all = await db_del_all_users()
    if delete_all:
        return {"status": "success"}
    else:
        raise HTTPException(status_code=400, detail="Error deleting users")


@app.delete('/api/v1/tickets', summary="Delete all tickets")
async def delete_all_tickets():
    delete_all = await db_del_all_tickets()
    if delete_all:
        return {"status": "success"}
    else:
        raise HTTPException(status_code=400, detail="Error deleting tickets")
