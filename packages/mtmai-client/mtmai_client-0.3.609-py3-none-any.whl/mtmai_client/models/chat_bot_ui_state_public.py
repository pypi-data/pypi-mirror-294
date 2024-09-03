from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.chat_bot_ui_state import ChatBotUiState


T = TypeVar("T", bound="ChatBotUiStatePublic")


@_attrs_define
class ChatBotUiStatePublic:
    """
    Attributes:
        ui_state (ChatBotUiState):
    """

    ui_state: "ChatBotUiState"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        ui_state = self.ui_state.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ui_state": ui_state,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.chat_bot_ui_state import ChatBotUiState

        d = src_dict.copy()
        ui_state = ChatBotUiState.from_dict(d.pop("ui_state"))

        chat_bot_ui_state_public = cls(
            ui_state=ui_state,
        )

        chat_bot_ui_state_public.additional_properties = d
        return chat_bot_ui_state_public

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
