from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from starlette.requests import Request
from starlette_admin.tools.iter import escape

from app.datebase import Base, int_pk, last_login, date_joined
from app.api.v1.users.schemas import UserRoles
from app.api.v1.subscription.models import Subscription


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int_pk]
    telegram_id: Mapped[int] = mapped_column(unique=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    role: Mapped[UserRoles] = mapped_column(default="user")
    last_login: Mapped[last_login]
    date_joined: Mapped[date_joined]
    subscription_id: Mapped[int] = mapped_column(ForeignKey('subscriptions.id', ondelete='SET NULL'), nullable=True)

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
            "last_login": self.last_login,
            "date_joined": self.date_joined,
            "subscription_id": self.subscription_id,
        }

    async def __admin_select2_repr__(self, request: Request) -> str:
        return f'<div><b>id:</b> <span>{escape(str(self.id))}</span> <b>username:</b> <span>{escape(self.username)}</span> <b>telegram_id:</b> <span>{escape(str(self.telegram_id))}</span></div>'
