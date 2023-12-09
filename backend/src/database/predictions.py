from typing import Any

from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base
from src.database.model import Model
from src.database.user import User


class Prediction(Base):
    __tablename__ = "prediction"

    model_id: Mapped[int] = mapped_column(ForeignKey("model.id"))
    model: Mapped[Model] = relationship("Model", back_populates="predictions")
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped[User] = relationship("User", back_populates="predictions")
    input: Mapped[dict[str, Any]] = mapped_column(JSON)
    output: Mapped[dict[str, Any]] = mapped_column(JSON)
