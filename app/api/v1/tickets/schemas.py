from enum import Enum
from typing import Optional

from pydantic import BaseModel, HttpUrl


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
