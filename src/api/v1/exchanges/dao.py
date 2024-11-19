from sqlalchemy import select, delete, update
from sqlalchemy.exc import SQLAlchemyError

from src.api.v1.exchanges.models import Exchange
from src.datebase import async_session_factory


async def init_exchanges():
    list_of_exchanges = ['Binance', 'Bybit', 'Paxful', 'OKX', 'GateIo']
    exchanges_to_insert = [Exchange(name=exchange) for exchange in list_of_exchanges]

    try:
        async with async_session_factory() as session:
            query = await session.execute(select(Exchange))
            existing_exchanges = query.scalars().all()

            if not existing_exchanges:
                session.add_all(exchanges_to_insert)
                await session.commit()
    except SQLAlchemyError as ex:
        print({'message': ex})
        await session.rollback()


async def db_get_all_exchanges():
    try:
        async with async_session_factory() as session:
            query = await session.execute(select(Exchange))
            all_exchanges = query.scalars().all()

            return all_exchanges
    except SQLAlchemyError as ex:
        print({'message': ex})
        await session.rollback()


async def db_get_exchange_by_any_filter(**filter_by):
    try:
        async with async_session_factory() as session:
            query = await session.execute(select(Exchange).filter_by(**filter_by))
            exchange = query.scalars().first()

            return exchange
    except SQLAlchemyError as ex:
        print({'message': ex})
        await session.rollback()


async def db_add_new_exchange(**filter_by):
    try:
        async with async_session_factory() as session:

            query = await session.execute(select(Exchange).filter_by(name=filter_by['name']))
            check_exchange = query.scalars().one_or_none()
            if check_exchange:
                return False

            new_exchange = Exchange(**filter_by)
            session.add(new_exchange)

            await session.commit()
            await session.refresh(new_exchange)

            return {'id': new_exchange.id,
                    'name': new_exchange.name,
                    }

    except SQLAlchemyError as ex:
        print({'message': ex})
        await session.rollback()


async def db_del_exchange(exchange_id: int):
    try:
        async with async_session_factory() as session:
            deleted_count = await session.execute(delete(Exchange).filter_by(id=exchange_id))
            await session.commit()

            return deleted_count.rowcount > 0
    except SQLAlchemyError as ex:
        print({'message': ex})
        await session.rollback()


async def db_upd_exchange(exchange_update_filter, new_data):
    exchange_id = exchange_update_filter.exchange_id

    try:
        async with async_session_factory() as session:
            query = await session.execute(select(Exchange).filter_by(id=exchange_id))
            check_exchange = query.scalars().one_or_none()

            if check_exchange:
                for key, value in new_data:
                    await session.execute(
                        update(Exchange).where(Exchange.id == exchange_id).values({key: value}))

                await session.commit()
                await session.refresh(check_exchange)
                return {'id': check_exchange.id, 'name': check_exchange.name}
    except SQLAlchemyError as ex:
        print({'message': ex})
        await session.rollback()
