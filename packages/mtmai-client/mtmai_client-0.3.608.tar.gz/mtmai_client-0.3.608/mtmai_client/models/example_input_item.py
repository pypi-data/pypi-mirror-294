from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ExampleInputItem")


@_attrs_define
class ExampleInputItem:
    """
    Attributes:
        title (str):
        description (str):
        content (str):
    """

    title: str
    description: str
    content: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        title = self.title

        description = self.description

        content = self.content

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "title": title,
                "description": description,
                "content": content,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        title = d.pop("title")

        description = d.pop("description")

        content = d.pop("content")

        example_input_item = cls(
            title=title,
            description=description,
            content=content,
        )

        example_input_item.additional_properties = d
        return example_input_item

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
