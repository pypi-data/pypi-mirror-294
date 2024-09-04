from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ui_messages_item_props import UiMessagesItemProps


T = TypeVar("T", bound="UiMessagesItem")


@_attrs_define
class UiMessagesItem:
    """
    Attributes:
        role (str):
        id (str):
        component (Union[Unset, str]):
        props (Union[Unset, UiMessagesItemProps]):
        thread_id (Union[Unset, str]):
    """

    role: str
    id: str
    component: Union[Unset, str] = UNSET
    props: Union[Unset, "UiMessagesItemProps"] = UNSET
    thread_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        role = self.role

        id = self.id

        component = self.component

        props: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.props, Unset):
            props = self.props.to_dict()

        thread_id = self.thread_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "role": role,
                "id": id,
            }
        )
        if component is not UNSET:
            field_dict["component"] = component
        if props is not UNSET:
            field_dict["props"] = props
        if thread_id is not UNSET:
            field_dict["thread_id"] = thread_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.ui_messages_item_props import UiMessagesItemProps

        d = src_dict.copy()
        role = d.pop("role")

        id = d.pop("id")

        component = d.pop("component", UNSET)

        _props = d.pop("props", UNSET)
        props: Union[Unset, UiMessagesItemProps]
        if isinstance(_props, Unset):
            props = UNSET
        else:
            props = UiMessagesItemProps.from_dict(_props)

        thread_id = d.pop("thread_id", UNSET)

        ui_messages_item = cls(
            role=role,
            id=id,
            component=component,
            props=props,
            thread_id=thread_id,
        )

        ui_messages_item.additional_properties = d
        return ui_messages_item

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
