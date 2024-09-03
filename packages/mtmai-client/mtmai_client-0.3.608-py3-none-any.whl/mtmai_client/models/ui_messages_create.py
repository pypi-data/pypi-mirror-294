from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ui_messages_create_props import UiMessagesCreateProps


T = TypeVar("T", bound="UiMessagesCreate")


@_attrs_define
class UiMessagesCreate:
    """
    Attributes:
        role (str):
        component (str):
        thread_id (str):
        props (Union[Unset, UiMessagesCreateProps]):
    """

    role: str
    component: str
    thread_id: str
    props: Union[Unset, "UiMessagesCreateProps"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        role = self.role

        component = self.component

        thread_id = self.thread_id

        props: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.props, Unset):
            props = self.props.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "role": role,
                "component": component,
                "thread_id": thread_id,
            }
        )
        if props is not UNSET:
            field_dict["props"] = props

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.ui_messages_create_props import UiMessagesCreateProps

        d = src_dict.copy()
        role = d.pop("role")

        component = d.pop("component")

        thread_id = d.pop("thread_id")

        _props = d.pop("props", UNSET)
        props: Union[Unset, UiMessagesCreateProps]
        if isinstance(_props, Unset):
            props = UNSET
        else:
            props = UiMessagesCreateProps.from_dict(_props)

        ui_messages_create = cls(
            role=role,
            component=component,
            thread_id=thread_id,
            props=props,
        )

        ui_messages_create.additional_properties = d
        return ui_messages_create

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
