from sqlalchemy.orm import Mapped, relationship

from app.datebase import Base, int_pk


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

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }
