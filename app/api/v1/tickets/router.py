from fastapi import APIRouter, HTTPException, Depends

from app.api.v1.tickets.schemas import TicketCreateFilter, GetTicketFilter
from app.api.v1.tickets.dao import *
from app.api.v1.users.auth import is_admin_user, is_staff_user
from app.api.v1.users.models import User

router = APIRouter()


@router.get('/tickets', summary="Get all tickets")
async def get_all_tickets():
    tickets = await db_get_all_tickets()
    if tickets:
        return {"status": "success", 'tickets': tickets}
    else:
        raise HTTPException(status_code=404, detail='Tickets not found')


@router.post('/ticket', summary="Set new ticket")
async def set_new_ticket(ticket: TicketCreateFilter):
    new_ticket = await db_add_new_ticket(**ticket.__dict__)
    if new_ticket:
        return {"status": "success", 'ticket_id': new_ticket}
    else:
        raise HTTPException(status_code=404, detail='Error added ticket')


@router.get('/ticket', summary="Get a filtered ticket")
async def get_filtered_ticket(filter_ticket: GetTicketFilter = Depends()):
    filters = {key: value for key, value in filter_ticket.__dict__.items() if value is not None}

    tickets = await db_get_filtered_ticket(**filters)
    if tickets:
        return {"status": "success", 'tickets': tickets}
    else:
        raise HTTPException(status_code=404, detail='Tickets not found')


@router.delete('/ticket/{ticket_id}', summary="Delete a ticket")
async def delete_ticket(ticket_id: int, _: User = Depends(is_staff_user)):
    delete_ticket = await db_del_ticket(ticket_id)
    if delete_ticket:
        return {"status": "success"}
    else:
        raise HTTPException(status_code=400, detail="Error deleting ticket")


@router.delete('/tickets', summary="Delete all tickets")
async def delete_all_tickets(_: User = Depends(is_admin_user)):
    delete_all = await db_del_all_tickets()
    if delete_all:
        return {"status": "success"}
    else:
        raise HTTPException(status_code=400, detail="Error deleting tickets")
