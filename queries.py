import random

from sqlalchemy import delete, select, update
from sqlalchemy.orm import sessionmaker

from utils import hash_password
from models import Exchanges, DebugTickets, engine, User, UserRoles

session_factory = sessionmaker(bind=engine)


def generate_random_ticket() -> dict:
    dict_of_tickets = {
        'username': 'John Doe',
        'price': random.randint(100, 300),
        'orders': random.randint(100, 300),
        'available': random.randint(100, 300),
        'max_limit': random.randint(100, 300),
        'min_limit': random.randint(1, 100),
        'rate': random.randint(1, 100),
        'pay_methods': {},
        'currency': random.choice(['USD', 'EUR']),
        'coin': random.choice(['USDT', 'BTC', 'ETH', 'USDC', 'DOGE']),
        'trade_type': random.choice(['BUY', 'SELL']),
        'link': 'https://#',
        'exchange_id': random.randint(1, 5),
    }
    return dict_of_tickets


def init_exchanges() -> None:
    list_of_exchanges = ['Binance', 'Bybit', 'Paxful', 'OKX', 'GateIo']
    exchanges_to_insert = [Exchanges(name=exchange) for exchange in list_of_exchanges]

    try:
        with session_factory() as session:
            if not session.query(Exchanges).all():
                session.add_all(exchanges_to_insert)
                session.commit()
    except Exception as ex:
        print(ex)
        session.rollback()


def init_debug_tickets() -> None:
    tickets_to_insert = [DebugTickets(**generate_random_ticket()) for _ in range(30)]

    try:
        with session_factory() as session:
            current_tickets = delete(DebugTickets)
            session.execute(current_tickets)

            session.add_all(tickets_to_insert)
            session.commit()
    except Exception as ex:
        print(ex)
        session.rollback()


def db_get_all_tickets():
    try:
        with session_factory() as session:
            all_tickets = session.query(DebugTickets).all()
            return all_tickets
    except Exception as ex:
        print(ex)
        session.rollback()


def db_get_filtered_ticket(coin, currency, trade_type):
    try:
        with session_factory() as session:
            filtered_tickets = session.query(DebugTickets).filter_by(coin=coin, currency=currency,
                                                                     trade_type=trade_type).all()
            return filtered_tickets

    except Exception as ex:
        print(ex)


def db_add_new_user(telegram_id, username, password, role):
    try:
        with session_factory() as session:
            new_user = User(telegram_id=telegram_id, username=username, password=hash_password(password), role=role)
            session.add(new_user)
            session.commit()
    except Exception as ex:
        print(ex)
        session.rollback()


def db_get_all_users():
    try:
        with session_factory() as session:
            all_users = session.query(User).all()
            return all_users
    except Exception as ex:
        print(ex)
        session.rollback()


def db_upd_user(user_update_filter, new_data):
    try:
        user_id = user_update_filter.user_id

        with session_factory() as session:
            check_user = session.query(User).filter_by(id=user_id).first()
            if check_user:
                for key, value in new_data:
                    if isinstance(value, UserRoles):
                        value = value.value
                    if key == 'password':
                        value = hash_password(value)
                    upd_query = update(User).where(User.id == user_id).values({key: value})
                    session.execute(upd_query)
                session.commit()
            else:
                raise ValueError('User does not exist')
    except Exception as ex:
        print(ex)
        session.rollback()