from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.datebase import int_pk, Base


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

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "subscription_type": self.subscription_type,
            "start_date": self.start_date,
            "end_date": self.end_date,
        }
