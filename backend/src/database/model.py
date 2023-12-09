from src.database.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.database.predictions import Prediction


class Model(Base):
    __tablename__ = "model"

    name: Mapped[str]
    cost: Mapped[float]
    description: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    predictions: Mapped[list["Prediction"]] = relationship("Prediction", back_populates="model")
