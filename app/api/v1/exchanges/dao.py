from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.api.v1.exchanges.models import Exchanges
from app.datebase import async_session_factory


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
