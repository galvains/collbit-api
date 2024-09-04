from fastapi import APIRouter, HTTPException

from app.api.v1.users.dao import *
from app.api.v1.users.schemas import UserRegistrationFilter, UserNewDataFilter, UserUpdateFilter

router = APIRouter()


@router.post('/user', summary="Set new user")
async def set_new_user(user: UserRegistrationFilter):
    new_user = await db_add_new_user(**user.__dict__)
    if new_user:
        return {"status": "success", 'user': new_user}
    else:
        raise HTTPException(status_code=400, detail='User already exists')


@router.get('/users', summary="Get all users")
async def get_all_users():
    users = await db_get_all_users()
    if users:
        return {"status": "success", 'users': users}
    else:
        raise HTTPException(status_code=404, detail='Users not found')


@router.get('/user/{user_id}', summary="Get a filtered user")
async def get_user(user_id: int):
    user = await db_get_user(user_id)
    if user:
        return {"status": "success", 'user': user}
    else:
        raise HTTPException(status_code=404, detail='User not found')


@router.put('/user', summary="Update a user")
async def update_user(user_update_filter: UserUpdateFilter, new_data: UserNewDataFilter):
    updater_user = await db_upd_user(user_update_filter, new_data)
    if updater_user:
        return {"status": "success", 'user': updater_user}
    else:
        raise HTTPException(status_code=404, detail='User not found')


@router.delete('/user/{user_id}', summary="Delete a user")
async def delete_user(user_id: int):
    delete = await db_del_user(user_id)
    if delete:
        return {"status": "success"}
    else:
        raise HTTPException(status_code=400, detail="Error deleting user")


@router.delete('/users', summary="Delete all users")
async def delete_all_users():
    delete_all = await db_del_all_users()
    if delete_all:
        return {"status": "success"}
    else:
        raise HTTPException(status_code=400, detail="Error deleting users")
