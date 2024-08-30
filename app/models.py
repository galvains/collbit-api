import os

from enum import Enum
from datetime import datetime
from typing import Optional, Annotated

from dotenv import load_dotenv

from pydantic import BaseModel, HttpUrl
from sqlalchemy import create_engine, ForeignKey, func
from sqlalchemy.types import JSON
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship

load_dotenv()
Base = declarative_base()
engine = create_engine(os.getenv('DATABASE_URL'))

int_pk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
date_joined = Annotated[datetime, mapped_column(server_default=func.now())]
last_login = Annotated[datetime, mapped_column(server_default=func.now(), onupdate=datetime.now)]


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

    id: Mapped[int_pk]
    telegram_id: Mapped[int] = mapped_column(unique=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    role: Mapped[str]
    is_subscriber: Mapped[bool] = mapped_column(default=False)
    last_login: Mapped[last_login]
    date_joined: Mapped[date_joined]

    subscription = relationship("Subscription", back_populates="user", uselist=False)

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, "
                f"telegram_id={self.telegram_id!r},"
                f"username={self.username!r})")

    def __repr__(self):
        return str(self)


class Subscription(Base):
    __tablename__ = 'subscriptions'

    id: Mapped[int_pk]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    subscription_type: Mapped[str]
    start_date: Mapped[datetime] = mapped_column(default=datetime.now)
    end_date: Mapped[datetime]

    user = relationship("User", back_populates="subscription")

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, "
                f"user_id={self.user_id!r},"
                f"subscription_type={self.subscription_type!r}),"
                f"start_date={self.start_date!r},"
                f"end_date={self.end_date!r})")

    def __repr__(self):
        return str(self)


class Exchanges(Base):
    __tablename__ = 'exchanges'

    id: Mapped[int_pk]
    name: Mapped[str]

    tickets = relationship("Tickets", back_populates="exchange")

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, "
                f"name={self.name!r}")

    def __repr__(self):
        return str(self)


class Tickets(Base):
    __tablename__ = 'tickets'

    id: Mapped[int_pk]
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
    time_create: Mapped[date_joined]
    exchange_id: Mapped[int] = mapped_column(ForeignKey('exchanges.id'))

    exchange = relationship("Exchanges", back_populates="tickets")

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, "
                f"username={self.username!r},"
                f"currency={self.currency!r}),"
                f"coin={self.coin!r},"
                f"trade_type={self.trade_type!r}),"
                f"link={self.link!r}")

    def __repr__(self):
        return str(self)
