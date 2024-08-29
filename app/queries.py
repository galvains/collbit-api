import random

from sqlalchemy import delete, update
from sqlalchemy.orm import sessionmaker

from app.utils import hash_password
from app.models import Exchanges, engine, User, UserRoles, Tickets

session_factory = sessionmaker(bind=engine)


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


def init_exchanges():
    list_of_exchanges = ['Binance', 'Bybit', 'Paxful', 'OKX', 'GateIo']
    exchanges_to_insert = [Exchanges(name=exchange) for exchange in list_of_exchanges]

    try:
        with session_factory() as session:
            if not session.query(Exchanges).all():
                session.add_all(exchanges_to_insert)
                session.commit()
    except Exception as ex:
        print({'message': ex})
        session.rollback()


def init_debug_tickets():
    tickets_to_insert = [Tickets(**generate_random_ticket()) for _ in range(30)]

    try:
        with session_factory() as session:
            current_tickets = delete(Tickets)
            session.execute(current_tickets)

            session.add_all(tickets_to_insert)
            session.commit()
    except Exception as ex:
        print({'message': ex})
        session.rollback()


def db_get_all_tickets():
    try:
        with session_factory() as session:
            all_tickets = session.query(Tickets).all()
            return all_tickets
    except Exception as ex:
        print({'message': ex})
        session.rollback()


def db_get_filtered_ticket(**kwargs):
    try:
        with session_factory() as session:
            for key, value in kwargs.items():
                if key != 'username':
                    kwargs[key] = value.value
            filtered_tickets = session.query(Tickets).filter_by(**kwargs).all()
            return filtered_tickets

    except Exception as ex:
        print({'message': ex})
        session.rollback()


def db_add_new_user(**kwargs):
    kwargs['password'] = hash_password(kwargs['password'])
    if isinstance(kwargs.get('role'), UserRoles):
        kwargs['role'] = kwargs['role'].value

    try:
        with session_factory() as session:
            new_user = User(**kwargs)
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
            return {'id': new_user.id, 'telegram_id': new_user.telegram_id, 'role': new_user.role}
    except Exception as ex:
        print({'message': ex})
        session.rollback()


def db_get_all_users():
    try:
        with session_factory() as session:
            all_users = session.query(User).all()
            return all_users
    except Exception as ex:
        print({'message': ex})
        session.rollback()


def db_upd_user(user_update_filter, new_data):
    try:
        user_id = user_update_filter.user_id

        with session_factory() as session:
            check_user = session.query(User).filter_by(id=user_id).one_or_none()
            if check_user:
                for key, value in new_data:
                    if isinstance(value, UserRoles):
                        value = value.value
                    if key == 'password':
                        value = hash_password(value)
                    upd_query = update(User).where(User.id == user_id).values({key: value})
                    session.execute(upd_query)
                session.commit()
                session.refresh(check_user)
                return {'id': check_user.id, 'telegram_id': check_user.telegram_id, 'role': check_user.role}
    except Exception as ex:
        print({'message': ex})
        session.rollback()


def db_get_user(user_id):
    try:
        with session_factory() as session:
            user = session.query(User).filter_by(id=user_id).first()
            return user
    except Exception as ex:
        print({'message': ex})
        session.rollback()


def db_add_new_ticket(**kwargs):
    kwargs['link'] = str(kwargs['link'])
    try:
        with session_factory() as session:
            new_ticket = Tickets(**kwargs)
            session.add(new_ticket)
            session.commit()
            return new_ticket.id
    except Exception as ex:
        print({'message': ex})
        session.rollback()


def db_del_ticket(ticket_id):
    try:
        with session_factory() as session:
            deleted_count = session.query(Tickets).filter_by(id=ticket_id).delete(synchronize_session='fetch')
            session.commit()
            return deleted_count > 0
    except Exception as ex:
        print({'message': ex})
        session.rollback()


def db_del_user(user_id):
    try:
        with session_factory() as session:
            deleted_count = session.query(User).filter_by(id=user_id).delete(synchronize_session='fetch')
            session.commit()
            return deleted_count > 0
    except Exception as ex:
        print({'message': ex})
        session.rollback()


def db_del_all_users():
    try:
        with session_factory() as session:
            deleted_count = session.query(User).delete(synchronize_session='fetch')
            session.commit()
            return deleted_count > 0
    except Exception as ex:
        print({'message': ex})
        session.rollback()
