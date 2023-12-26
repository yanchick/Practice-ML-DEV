from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base

if TYPE_CHECKING:
    from src.database.predictions import Prediction


class User(Base):
    __tablename__ = "user"

    username: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[str]
    balance: Mapped[float] = mapped_column(default=0.0)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    predictions: Mapped[list["Prediction"]] = relationship("Prediction", back_populates="user")

    def __repr__(self) -> str:
        return f"<User {self.username}>"

    def to_dict(self) -> dict[str, str | float | bool]:
        return {
            "username": self.username,
            "balance": self.balance,
            "is_active": self.is_active,
            "is_superuser": self.is_superuser,
        }
