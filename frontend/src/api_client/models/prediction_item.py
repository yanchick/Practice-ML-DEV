from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="PredictionItem")


@_attrs_define
class PredictionItem:
    """
    Attributes:
        id (int):
        predicted_model_id (int):
        result (Union[None, int]):
        input_data (str):
    """

    id: int
    predicted_model_id: int
    result: None | int
    input_data: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        predicted_model_id = self.predicted_model_id

        result: None | int
        result = self.result

        input_data = self.input_data

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "predicted_model_id": predicted_model_id,
                "result": result,
                "input_data": input_data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        predicted_model_id = d.pop("predicted_model_id")

        def _parse_result(data: object) -> None | int:
            if data is None:
                return data
            return cast(None | int, data)

        result = _parse_result(d.pop("result"))

        input_data = d.pop("input_data")

        prediction_item = cls(
            id=id,
            predicted_model_id=predicted_model_id,
            result=result,
            input_data=input_data,
        )

        prediction_item.additional_properties = d
        return prediction_item

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
