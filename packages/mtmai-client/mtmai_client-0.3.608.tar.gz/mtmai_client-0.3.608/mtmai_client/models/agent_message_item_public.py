from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AgentMessageItemPublic")


@_attrs_define
class AgentMessageItemPublic:
    """
    Attributes:
        agent_id (str):
        content (Union[None, Unset, str]):
        role (Union[None, Unset, str]):  Default: 'user'.
        msg_ypte (Union[None, Unset, str]):  Default: 'msg'.
    """

    agent_id: str
    content: Union[None, Unset, str] = UNSET
    role: Union[None, Unset, str] = "user"
    msg_ypte: Union[None, Unset, str] = "msg"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        agent_id = self.agent_id

        content: Union[None, Unset, str]
        if isinstance(self.content, Unset):
            content = UNSET
        else:
            content = self.content

        role: Union[None, Unset, str]
        if isinstance(self.role, Unset):
            role = UNSET
        else:
            role = self.role

        msg_ypte: Union[None, Unset, str]
        if isinstance(self.msg_ypte, Unset):
            msg_ypte = UNSET
        else:
            msg_ypte = self.msg_ypte

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "agent_id": agent_id,
            }
        )
        if content is not UNSET:
            field_dict["content"] = content
        if role is not UNSET:
            field_dict["role"] = role
        if msg_ypte is not UNSET:
            field_dict["msg_ypte"] = msg_ypte

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        agent_id = d.pop("agent_id")

        def _parse_content(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        content = _parse_content(d.pop("content", UNSET))

        def _parse_role(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        role = _parse_role(d.pop("role", UNSET))

        def _parse_msg_ypte(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        msg_ypte = _parse_msg_ypte(d.pop("msg_ypte", UNSET))

        agent_message_item_public = cls(
            agent_id=agent_id,
            content=content,
            role=role,
            msg_ypte=msg_ypte,
        )

        agent_message_item_public.additional_properties = d
        return agent_message_item_public

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
