from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.prediction_item import PredictionItem


T = TypeVar("T", bound="PredictionScheme")


@_attrs_define
class PredictionScheme:
    """
    Attributes:
        predictions (List['PredictionItem']):
    """

    predictions: list["PredictionItem"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        predictions = []
        for predictions_item_data in self.predictions:
            predictions_item = predictions_item_data.to_dict()
            predictions.append(predictions_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "predictions": predictions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.prediction_item import PredictionItem

        d = src_dict.copy()
        predictions = []
        _predictions = d.pop("predictions")
        for predictions_item_data in _predictions:
            predictions_item = PredictionItem.from_dict(predictions_item_data)

            predictions.append(predictions_item)

        prediction_scheme = cls(
            predictions=predictions,
        )

        prediction_scheme.additional_properties = d
        return prediction_scheme

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
