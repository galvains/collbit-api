from sqlalchemy import delete, select
from sqlalchemy.exc import SQLAlchemyError

from app.api.v1.tickets.models import Ticket
from app.datebase import async_session_factory
from app.utils import generate_random_ticket


async def init_debug_tickets():
    tickets_to_insert = [Ticket(**generate_random_ticket()) for _ in range(30)]

    try:
        async with async_session_factory() as session:
            await session.execute(delete(Ticket))

            session.add_all(tickets_to_insert)
            await session.commit()
    except SQLAlchemyError as ex:
        print({'message': ex})
        await session.rollback()


async def db_get_all_tickets():
    try:
        async with async_session_factory() as session:
            query = await session.execute(select(Ticket))
            existing_tickets = query.scalars().all()

            return existing_tickets
    except SQLAlchemyError as ex:
        print({'message': ex})
        await session.rollback()


async def db_get_filtered_ticket(**filter_by):
    try:
        async with async_session_factory() as session:
            for key, value in filter_by.items():

                if key != 'username':
                    filter_by[key] = value.value

            query = await session.execute(select(Ticket).filter_by(**filter_by))
            filtered_tickets = query.scalars().all()

            return filtered_tickets

    except SQLAlchemyError as ex:
        print({'message': ex})
        await session.rollback()


async def db_add_new_ticket(**filter_by):
    filter_by['link'] = str(filter_by['link'])
    try:
        async with async_session_factory() as session:
            new_ticket = Ticket(**filter_by)
            session.add(new_ticket)
            await session.commit()
            return new_ticket.id
    except SQLAlchemyError as ex:
        print({'message': ex})
        await session.rollback()


async def db_del_ticket(ticket_id):
    try:
        async with async_session_factory() as session:
            deleted_count = await session.execute(delete(Ticket).filter_by(id=ticket_id))
            await session.commit()

            return deleted_count.rowcount > 0
    except SQLAlchemyError as ex:
        print({'message': ex})
        await session.rollback()


async def db_del_all_tickets():
    try:
        async with async_session_factory() as session:
            deleted_count = await session.execute(delete(Ticket))
            await session.commit()

            return deleted_count.rowcount > 0
    except Exception as ex:
        print({'message': ex})
        await session.rollback()
