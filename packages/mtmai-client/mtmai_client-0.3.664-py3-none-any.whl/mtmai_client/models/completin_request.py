from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CompletinRequest")


@_attrs_define
class CompletinRequest:
    """
    Attributes:
        prompt (str):
        thread_id (Union[None, Unset, str]):
        option (Union[None, Unset, str]):
    """

    prompt: str
    thread_id: Union[None, Unset, str] = UNSET
    option: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        prompt = self.prompt

        thread_id: Union[None, Unset, str]
        if isinstance(self.thread_id, Unset):
            thread_id = UNSET
        else:
            thread_id = self.thread_id

        option: Union[None, Unset, str]
        if isinstance(self.option, Unset):
            option = UNSET
        else:
            option = self.option

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "prompt": prompt,
            }
        )
        if thread_id is not UNSET:
            field_dict["thread_id"] = thread_id
        if option is not UNSET:
            field_dict["option"] = option

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        prompt = d.pop("prompt")

        def _parse_thread_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        thread_id = _parse_thread_id(d.pop("thread_id", UNSET))

        def _parse_option(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        option = _parse_option(d.pop("option", UNSET))

        completin_request = cls(
            prompt=prompt,
            thread_id=thread_id,
            option=option,
        )

        completin_request.additional_properties = d
        return completin_request

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
