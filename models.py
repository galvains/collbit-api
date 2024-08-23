import os

from datetime import datetime
from dotenv import load_dotenv

from sqlalchemy import create_engine, ForeignKey, Integer
from sqlalchemy.types import JSON
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship

load_dotenv()
Base = declarative_base()
engine = create_engine(os.getenv('DATABASE_URL'))


class Users(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id: Mapped[int]
    username: Mapped[str]
    email: Mapped[str] = mapped_column(nullable=True)
    password: Mapped[str]
    is_superuser: Mapped[bool] = mapped_column(default=False)
    is_staff: Mapped[bool]
    is_active: Mapped[bool]
    is_subscriber: Mapped[bool] = mapped_column(default=False)
    last_login: Mapped[datetime]
    date_joined: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    def __repr__(self):
        return f"{self.username!r}"


class Tickets(Base):
    __tablename__ = 'tickets'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str]
    price: Mapped[float]
    orders: Mapped[int]
    available: Mapped[float]
    max_limit: Mapped[float]
    min_limit: Mapped[float]
    rate: Mapped[float]
    pay_methods: Mapped[dict] = mapped_column(JSON, nullable=False, server_default='{}')
    currency: Mapped[str]
    coin: Mapped[str]
    trade_type: Mapped[str]
    link: Mapped[str]
    time_create: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    # exchange_id = mapped_column(Integer, ForeignKey('exchanges.id'))
    # exchange = relationship("Exchanges", back_populates="tickets")

    def __repr__(self):
        return f"{self.__dict__!r}"


class Exchanges(Base):
    __tablename__ = 'exchanges'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]

    tickets = relationship("DebugTickets", back_populates="exchange")

    def __repr__(self):
        return f"{self.__dict__!r}"


class DebugTickets(Base):
    __tablename__ = 'debug_tickets'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str]
    price: Mapped[float]
    orders: Mapped[int]
    available: Mapped[float]
    max_limit: Mapped[float]
    min_limit: Mapped[float]
    rate: Mapped[float]
    pay_methods: Mapped[dict] = mapped_column(JSON, nullable=False, server_default='{}')
    currency: Mapped[str]
    coin: Mapped[str]
    trade_type: Mapped[str]
    link: Mapped[str]
    time_create: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    exchange_id = mapped_column(Integer, ForeignKey('exchanges.id'))

    exchange = relationship("Exchanges", back_populates="tickets")

    def __repr__(self):
        return f"{self.__dict__!r}"
