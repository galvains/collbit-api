from sqlalchemy import ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.api.v1.tickets.schemas import CurrencyTypes, CoinTypes, TradeTypes
from src.datebase import Base, int_pk, date_joined


class Ticket(Base):
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
    exchange_id: Mapped[int] = mapped_column(ForeignKey('exchanges.id', ondelete="CASCADE"), nullable=False)

    exchange = relationship("Exchange", back_populates="tickets")

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, "
                f"username={self.username!r},"
                f"currency={self.currency!r}),"
                f"coin={self.coin!r},"
                f"trade_type={self.trade_type!r}),"
                f"link={self.link!r}")

    def __repr__(self):
        return str(self)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "price": self.price,
            "orders": self.orders,
            "available": self.available,
            "max_limit": self.max_limit,
            "min_limit": self.min_limit,
            "rate": self.rate,
            "pay_methods": self.pay_methods,
            "currency": self.currency,
            "coin": self.coin,
            "trade_type": self.trade_type,
            "link": self.link,
            "time_create": self.time_create,
            "exchange_id": self.exchange_id,
        }
