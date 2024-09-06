from sqlalchemy import delete, select
from sqlalchemy.exc import SQLAlchemyError

from app.api.v1.tickets.models import Tickets
from app.datebase import async_session_factory
from app.utils import generate_random_ticket


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


async def db_del_all_tickets():
    try:
        async with async_session_factory() as session:
            deleted_count = await session.execute(delete(Tickets))
            await session.commit()

            return deleted_count.rowcount > 0
    except Exception as ex:
        print({'message': ex})
        await session.rollback()