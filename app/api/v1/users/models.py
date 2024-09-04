from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.datebase import Base, int_pk, last_login, date_joined
from app.api.v1.subscription.models import Subscription


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

    def to_dict(self):
        return {
            "id": self.id,
            "telegram_id": self.telegram_id,
            "username": self.username,
            "role": self.role,
            "is_subscriber": self.is_subscriber,
            "last_login": self.last_login,
            "date_joined": self.date_joined,
        }
