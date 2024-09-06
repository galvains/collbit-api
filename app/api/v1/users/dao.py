from datetime import datetime

from sqlalchemy import select, update, delete, or_
from sqlalchemy.exc import SQLAlchemyError

from app.api.v1.users.models import User
from app.api.v1.users.schemas import UserRoles
from app.datebase import async_session_factory
from app.api.v1.users.auth import get_password_hash


async def create_admin():
    await db_del_user(telegram_id=1000)
    admin_payload = {
        "telegram_id": 1000,
        "username": "admin",
        "password": get_password_hash("admin"),
        "role": "admin"
    }
    try:
        async with async_session_factory() as session:
            admin = User(**admin_payload)
            session.add(admin)
            await session.commit()
    except SQLAlchemyError as ex:
        print({'message': ex})
        await session.rollback()


async def db_add_new_user(**kwargs):
    kwargs['password'] = get_password_hash(kwargs['password'])

    if isinstance(kwargs.get('role'), UserRoles):
        kwargs['role'] = kwargs['role'].value

    try:
        async with async_session_factory() as session:
            new_user = User(**kwargs)
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            return {'id': new_user.id, 'telegram_id': new_user.telegram_id, 'role': new_user.role}
    except SQLAlchemyError as ex:
        print({'message': ex})
        await session.rollback()


async def db_get_all_users():
    try:
        async with async_session_factory() as session:
            query = await session.execute(select(User))
            all_users = query.scalars().all()

            return all_users
    except SQLAlchemyError as ex:
        print({'message': ex})
        await session.rollback()


async def db_upd_user(user_update_filter, new_data):
    try:

        user_id = user_update_filter.user_id

        async with async_session_factory() as session:
            query = await session.execute(select(User).filter_by(id=user_id))
            check_user = query.scalars().one_or_none()

            if check_user:
                for key, value in new_data:

                    if isinstance(value, UserRoles):
                        value = value.value
                    if isinstance(value, datetime):
                        value = value.replace(tzinfo=None)
                    if key == 'password':
                        value = get_password_hash(value)

                    await session.execute(update(User).where(User.id == user_id).values({key: value}))

                await session.commit()
                await session.refresh(check_user)
                return {'id': check_user.id, 'telegram_id': check_user.telegram_id, 'role': check_user.role}
    except SQLAlchemyError as ex:
        print({'message': ex})
        await session.rollback()


async def db_get_user_by_any_filter(**filter_by):
    try:
        async with async_session_factory() as session:
            query = await session.execute(select(User).filter_by(**filter_by))
            user = query.scalars().first()
            return user
    except SQLAlchemyError as ex:
        print({'message': ex})
        await session.rollback()


async def db_del_user(**filter_by):
    try:
        async with async_session_factory() as session:
            deleted_count = await session.execute(delete(User).filter_by(**filter_by))
            await session.commit()

            return deleted_count.rowcount > 0
    except SQLAlchemyError as ex:
        print({'message': ex})
        await session.rollback()


async def db_del_all_non_admin_users():
    try:
        async with async_session_factory() as session:
            stmt = delete(User).where(or_(User.role == 'user', User.role == 'staff'))
            deleted_count = await session.execute(stmt)
            await session.commit()

            return deleted_count.rowcount > 0
    except Exception as ex:
        print({'message': ex})
        await session.rollback()
