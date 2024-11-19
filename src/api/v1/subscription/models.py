from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.api.v1.subscription.schemas import *
from src.datebase import Base, int_pk


class Subscription(Base):
    __tablename__ = 'subscriptions'

    id: Mapped[int_pk]
    subscription_type: Mapped[TypesSubscription]
    start_date: Mapped[datetime] = mapped_column(onupdate=datetime.now, server_default=func.now())
    end_date: Mapped[datetime]

    user = relationship("User", back_populates="subscription", foreign_keys='User.subscription_id')

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, "
                f"subscription_type={self.subscription_type!r}),"
                f"start_date={self.start_date!r},"
                f"end_date={self.end_date!r})")

    def __repr__(self):
        return str(self)

    def to_dict(self):
        return {
            "id": self.id,
            "subscription_type": self.subscription_type,
            "start_date": self.start_date,
            "end_date": self.end_date,
        }
