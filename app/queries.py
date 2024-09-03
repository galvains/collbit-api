import random

from datetime import datetime
from sqlalchemy import delete, update, select
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from app.utils import hash_password
from app.models import Exchanges, engine, User, UserRoles, Tickets

async_session_factory = async_sessionmaker(bind=engine, expire_on_commit=False)


def generate_random_ticket() -> dict:
    dict_of_tickets = {
        'username': 'John_Doe',
        'price': random.randint(100, 300),
        'orders': random.randint(100, 300),
        'available': random.randint(100, 300),
        'max_limit': random.randint(100, 300),
        'min_limit': random.randint(1, 100),
        'rate': random.randint(1, 100),
        'pay_methods': {},
        'currency': random.choice(['usd', 'eur']),
        'coin': random.choice(['usdt', 'btc', 'eth', 'usdc', 'doge']),
        'trade_type': random.choice(['buy', 'sell']),
        'link': 'https://#',
        'exchange_id': random.randint(1, 5),
    }
    return dict_of_tickets


async def init_exchanges():
    list_of_exchanges = ['Binance', 'Bybit', 'Paxful', 'OKX', 'GateIo']
    exchanges_to_insert = [Exchanges(name=exchange) for exchange in list_of_exchanges]

    try:
        async with async_session_factory() as session:
            query = await session.execute(select(Exchanges))
            existing_exchanges = query.scalars().all()

            if not existing_exchanges:
                session.add_all(exchanges_to_insert)
                await session.commit()
    except SQLAlchemyError as ex:
        print({'message': ex})
        await session.rollback()


async def init_debug_tickets():
    tickets_to_insert = [Tickets(**generate_random_ticket()) for _ in range(30)]

    try:
        async with async_session_factory() as session:
            await session.execute(delete(Tickets))

            session.add_all(tickets_to_insert)
            await session.commit()
    except SQLAlchemyError as ex:
        print({'message': ex})
        await session.rollback()


async def db_get_all_tickets():
    try:
        async with async_session_factory() as session:
            query = await session.execute(select(Tickets))
            existing_tickets = query.scalars().all()

            return existing_tickets
    except SQLAlchemyError as ex:
        print({'message': ex})
        await session.rollback()


async def db_get_filtered_ticket(**kwargs):
    try:
        async with async_session_factory() as session:
            for key, value in kwargs.items():
                if key != 'username':
                    kwargs[key] = value.value

            query = await session.execute(select(Tickets).filter_by(**kwargs))
            filtered_tickets = query.scalars().all()

            return filtered_tickets

    except SQLAlchemyError as ex:
        print({'message': ex})
        await session.rollback()


async def db_add_new_user(**kwargs):
    kwargs['password'] = hash_password(kwargs['password'])
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
                        value = hash_password(value)

                    await session.execute(update(User).where(User.id == user_id).values({key: value}))

                await session.commit()
                await session.refresh(check_user)
                return {'id': check_user.id, 'telegram_id': check_user.telegram_id, 'role': check_user.role}
    except SQLAlchemyError as ex:
        print({'message': ex})
        await session.rollback()


async def db_get_user(user_id):
    try:
        async with async_session_factory() as session:
            query = await session.execute(select(User).filter_by(id=user_id))
            user = query.scalars().first()
            return user
    except SQLAlchemyError as ex:
        print({'message': ex})
        await session.rollback()


async def db_add_new_ticket(**kwargs):
    kwargs['link'] = str(kwargs['link'])
    try:
        async with async_session_factory() as session:
            new_ticket = Tickets(**kwargs)
            session.add(new_ticket)
            await session.commit()
            return new_ticket.id
    except SQLAlchemyError as ex:
        print({'message': ex})
        await session.rollback()


async def db_del_ticket(ticket_id):
    try:
        async with async_session_factory() as session:
            deleted_count = await session.execute(delete(Tickets).filter_by(id=ticket_id))
            await session.commit()

            return deleted_count.rowcount > 0
    except SQLAlchemyError as ex:
        print({'message': ex})
        await session.rollback()


async def db_del_user(user_id):
    try:
        async with async_session_factory() as session:
            deleted_count = await session.execute(delete(User).filter_by(id=user_id))
            await session.commit()

            return deleted_count.rowcount > 0
    except SQLAlchemyError as ex:
        print({'message': ex})
        await session.rollback()


async def db_del_all_users():
    try:
        async with async_session_factory() as session:
            deleted_count = await session.execute(delete(User))
            await session.commit()

            return deleted_count.rowcount > 0
    except Exception as ex:
        print({'message': ex})
        await session.rollback()


async def db_del_all_tickets():
    try:
        async with async_session_factory() as session:
            deleted_count = await session.execute(delete(Tickets))
            await session.commit()

            return deleted_count.rowcount > 0
    except Exception as ex:
        print({'message': ex})
        await session.rollback()
