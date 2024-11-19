from fastapi import APIRouter, HTTPException, Depends

from src.api.v1.exchanges.schemas import *
from src.api.v1.exchanges.dao import *
from src.api.v1.users.auth import is_admin_user
from src.api.v1.users.models import User

router = APIRouter()


@router.get("/exchanges", summary="Get all exchanges")
async def get_all_exchanges():
    exchanges = await db_get_all_exchanges()
    if exchanges:
        return {"status": "success", 'exchanges': exchanges}
    else:
        raise HTTPException(status_code=404, detail='Exchanges not found')


@router.get("/exchange/{exchange_id}", summary="Get exchange")
async def get_all_exchanges(exchange_id: int):
    exchange = await db_get_exchange_by_any_filter(id=exchange_id)
    if exchange:
        return {"status": "success", 'exchange': exchange}
    else:
        raise HTTPException(status_code=404, detail='Exchange not found')


@router.post("/exchange", summary="Set new exchange")
async def create_exchange(exchange: ExchangeCreateFilter, _: User = Depends(is_admin_user)):
    new_exchange = await db_add_new_exchange(**exchange.model_dump())
    if new_exchange:
        return {"status": "success", 'exchange': new_exchange}
    else:
        raise HTTPException(status_code=404, detail='Error added exchange')


@router.delete('/exchange/{exchange_id}', summary="Delete a exchange")
async def delete_exchange(exchange_id: int, _: User = Depends(is_admin_user)):
    delete_exchange = await db_del_exchange(exchange_id)
    if delete_exchange:
        return {"status": "success"}
    else:
        raise HTTPException(status_code=400, detail="Error deleting exchange")


@router.put('/exchange', summary="Update a exchange")
async def update_exchange(exchange_update_filter: ExchangeUpdateFilter,
                          new_data: ExchangeNewDataFilter, _: User = Depends(is_admin_user)):
    updater_exchange = await db_upd_exchange(exchange_update_filter, new_data)
    if updater_exchange:
        return {"status": "success", 'exchange': updater_exchange}
    else:
        raise HTTPException(status_code=404, detail='Exchange not found')
