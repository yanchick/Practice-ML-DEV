from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base
from src.database.model import Model
from src.database.user import User


class PredictionClass(Base):
    __tablename__ = "prediction_class"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    predictions: Mapped[list["Prediction"]] = relationship("Prediction", back_populates="predicted_class")

    def __repr__(self) -> str:
        return f"<PredictionClass(id={self.id}, name={self.name})>"


class Prediction(Base):
    __tablename__ = "prediction"

    model_id: Mapped[int] = mapped_column(ForeignKey("model.id"))
    model: Mapped[Model] = relationship("Model", back_populates="predictions")
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), index=True)
    user: Mapped[User] = relationship("User", back_populates="predictions")
    input_data: Mapped[str] = mapped_column(nullable=False)
    predicted_class_id: Mapped[int | None] = mapped_column(ForeignKey("prediction_class.id"), nullable=True)
    predicted_class: Mapped[PredictionClass] = relationship("PredictionClass", back_populates="predictions")

    def __repr__(self) -> str:
        return (
            f"<Prediction(id={self.id}, model_id={self.model_id}, "
            f"user_id={self.user_id}, input_data={self.input_data}, predicted_class_id={self.predicted_class_id})>"
        )
