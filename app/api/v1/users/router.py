from fastapi import APIRouter, HTTPException, Depends

from app.api.v1.users.dao import db_get_all_users, db_get_user_by_any_filter, db_upd_user, db_del_user, \
    db_del_all_non_admin_users
from app.api.v1.users.schemas import UserNewDataFilter, UserUpdateFilter
from app.api.v1.users.models import User
from app.api.v1.users.auth import is_staff_user, is_admin_user

router = APIRouter()


@router.get('/users', summary="Get all users")
async def get_all_users(_: User = Depends(is_staff_user)):
    users = await db_get_all_users()
    if users:
        return {"status": "success", 'users': users}
    else:
        raise HTTPException(status_code=404, detail='Users not found')


@router.get('/user/{user_id}', summary="Get a filtered user")
async def get_user(user_id: int, _: User = Depends(is_staff_user)):
    user = await db_get_user_by_any_filter(id=user_id)
    if user:
        return {"status": "success", 'user': user}
    else:
        raise HTTPException(status_code=404, detail='User not found')


@router.put('/user', summary="Update a user")
async def update_user(user_update_filter: UserUpdateFilter, new_data: UserNewDataFilter,
                      _: User = Depends(is_staff_user)):
    query = await db_get_user_by_any_filter(id=user_update_filter.user_id)
    check_updated_user_role = query.to_dict()['role']

    if _.role == 'staff':
        if check_updated_user_role in ['staff', 'admin'] or new_data.role.value != check_updated_user_role:
            raise HTTPException(status_code=403, detail='You are not an admin')

    updated_user = await db_upd_user(user_update_filter, new_data)
    if updated_user:
        return {"status": "success", 'user': updated_user}
    else:
        raise HTTPException(status_code=404, detail='User not found')


@router.delete('/user/{user_id}', summary="Delete a user")
async def delete_user(user_id: int, _: User = Depends(is_admin_user)):
    delete = await db_del_user(user_id)
    if delete:
        return {"status": "success"}
    else:
        raise HTTPException(status_code=400, detail="Error deleting user")


@router.delete('/users', summary="Delete all non-admin users")
async def delete_all_non_admin_users(_: User = Depends(is_admin_user)):
    delete_all = await db_del_all_non_admin_users()
    if delete_all:
        return {"status": "success"}
    else:
        raise HTTPException(status_code=400, detail="Error deleting users")
