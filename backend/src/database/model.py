from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base

if TYPE_CHECKING:
    from src.database.predictions import Prediction


class Model(Base):
    __tablename__ = "model"

    name: Mapped[str]
    cost: Mapped[float]
    description: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    predictions: Mapped[list["Prediction"]] = relationship("Prediction", back_populates="model")

    def __repr__(self) -> str:
        return (
            f"<Model(id={self.id}, name={self.name}, "
            f"cost={self.cost}, description={self.description}, is_active={self.is_active})>"
        )
