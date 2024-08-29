import os

from enum import Enum
from datetime import datetime
from typing import Optional, Any

from dotenv import load_dotenv

from pydantic import BaseModel, HttpUrl
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.types import JSON
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship

load_dotenv()
Base = declarative_base()
engine = create_engine(os.getenv('DATABASE_URL'))


class UserRoles(Enum):
    user = 'user'
    admin = 'admin'
    staff = 'staff'


class TypesSubscription(Enum):
    lite = 'lite'
    medium = 'medium'
    hard = 'hard'


class CoinTypes(Enum):
    usdt = 'usdt'
    btc = 'btc'
    eth = 'eth'
    usdc = 'usdc'
    doge = 'doge'


class TradeTypes(Enum):
    buy = 'buy'
    sell = 'sell'


class CurrencyTypes(Enum):
    usd = 'usd'
    eur = 'eur'
    rub = 'rub'
    uah = 'uah'


class GetTicketFilter(BaseModel):
    username: Optional[str]
    coin: Optional[CoinTypes]
    currency: Optional[CurrencyTypes]
    trade_type: Optional[TradeTypes]


class SubscriptionCreateFilter(BaseModel):
    user_id: int
    subscription_type: TypesSubscription
    end_date: datetime


class TicketCreateFilter(BaseModel):
    username: str
    price: float
    orders: int
    available: float
    max_limit: float
    min_limit: float
    rate: float
    pay_methods: dict[str, str]
    currency: CurrencyTypes
    coin: CoinTypes
    trade_type: TradeTypes
    link: HttpUrl
    exchange_id: int


class TicketDeleteFilter(BaseModel):
    key: str
    value: Any


class UserRegistrationFilter(BaseModel):
    telegram_id: int
    username: str
    password: str | None
    role: UserRoles


class UserUpdateFilter(BaseModel):
    user_id: int


class UserNewDataFilter(BaseModel):
    username: str
    password: str
    role: UserRoles
    is_subscriber: bool
    last_login: datetime


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(unique=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    role: Mapped[str]
    is_subscriber: Mapped[bool] = mapped_column(default=False)
    last_login: Mapped[datetime] = mapped_column(nullable=True)
    date_joined: Mapped[datetime] = mapped_column(default=datetime.now)

    subscription = relationship("Subscription", back_populates="user", uselist=False)

    def __repr__(self):
        return f"{self.username!r}"


class Subscription(Base):
    __tablename__ = 'subscriptions'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    subscription_type: Mapped[str]
    start_date: Mapped[datetime] = mapped_column(default=datetime.now)
    end_date: Mapped[datetime]

    user = relationship("User", back_populates="subscription")

    def __repr__(self):
        return f"{self.user_id}: {self.subscription_type}"


class Exchanges(Base):
    __tablename__ = 'exchanges'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]

    tickets = relationship("Tickets", back_populates="exchange")

    def __repr__(self):
        return f"{self.__dict__!r}"


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
    currency: Mapped[CurrencyTypes]
    coin: Mapped[CoinTypes]
    trade_type: Mapped[TradeTypes]
    link: Mapped[str]
    time_create: Mapped[datetime] = mapped_column(default=datetime.now)
    exchange_id: Mapped[int] = mapped_column(ForeignKey('exchanges.id'))

    exchange = relationship("Exchanges", back_populates="tickets")

    def __repr__(self):
        return f"{self.__dict__!r}"
