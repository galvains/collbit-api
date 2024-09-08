from sqlalchemy.orm import Mapped, relationship, mapped_column

from app.datebase import Base, int_pk


class Exchange(Base):
    __tablename__ = 'exchanges'

    id: Mapped[int_pk]
    name: Mapped[str] = mapped_column(unique=True, nullable=False)

    tickets = relationship("Ticket", back_populates="exchange")

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
