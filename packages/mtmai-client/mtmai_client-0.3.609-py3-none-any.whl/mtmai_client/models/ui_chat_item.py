from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ui_chat_item_props_type_0 import UiChatItemPropsType0


T = TypeVar("T", bound="UiChatItem")


@_attrs_define
class UiChatItem:
    """
    Attributes:
        id (Union[None, Unset, str]):
        component (Union[None, Unset, str]):
        props (Union['UiChatItemPropsType0', None, Unset]):
    """

    id: Union[None, Unset, str] = UNSET
    component: Union[None, Unset, str] = UNSET
    props: Union["UiChatItemPropsType0", None, Unset] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.ui_chat_item_props_type_0 import UiChatItemPropsType0

        id: Union[None, Unset, str]
        if isinstance(self.id, Unset):
            id = UNSET
        else:
            id = self.id

        component: Union[None, Unset, str]
        if isinstance(self.component, Unset):
            component = UNSET
        else:
            component = self.component

        props: Union[Dict[str, Any], None, Unset]
        if isinstance(self.props, Unset):
            props = UNSET
        elif isinstance(self.props, UiChatItemPropsType0):
            props = self.props.to_dict()
        else:
            props = self.props

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if component is not UNSET:
            field_dict["component"] = component
        if props is not UNSET:
            field_dict["props"] = props

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.ui_chat_item_props_type_0 import UiChatItemPropsType0

        d = src_dict.copy()

        def _parse_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        id = _parse_id(d.pop("id", UNSET))

        def _parse_component(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        component = _parse_component(d.pop("component", UNSET))

        def _parse_props(data: object) -> Union["UiChatItemPropsType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                props_type_0 = UiChatItemPropsType0.from_dict(data)

                return props_type_0
            except:  # noqa: E722
                pass
            return cast(Union["UiChatItemPropsType0", None, Unset], data)

        props = _parse_props(d.pop("props", UNSET))

        ui_chat_item = cls(
            id=id,
            component=component,
            props=props,
        )

        ui_chat_item.additional_properties = d
        return ui_chat_item

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
