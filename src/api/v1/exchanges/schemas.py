from pydantic import BaseModel


class ExchangeCreateFilter(BaseModel):
    name: str


class ExchangeUpdateFilter(BaseModel):
    exchange_id: int


class ExchangeNewDataFilter(BaseModel):
    name: str
