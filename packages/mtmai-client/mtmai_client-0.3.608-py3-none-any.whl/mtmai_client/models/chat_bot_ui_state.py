from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.example_input_item import ExampleInputItem
    from ..models.ui_chat_item import UiChatItem
    from ..models.ui_chat_message_item import UIChatMessageItem


T = TypeVar("T", bound="ChatBotUiState")


@_attrs_define
class ChatBotUiState:
    """
    Attributes:
        agent (Union[None, Unset, str]):
        is_open_agent_rag_view (Union[None, Unset, bool]):
        thread_id (Union[None, Unset, str]):
        agent_url_base (Union[None, Unset, str]):
        graph_image_url (Union[None, Unset, str]):
        is_dev (Union[None, Unset, bool]):
        is_open_rag_ui (Union[None, Unset, bool]):
        is_open_search_view (Union[None, Unset, bool]):
        is_open_mtm_editor (Union[None, Unset, bool]):
        uichatitems (Union[List['UIChatMessageItem'], None, Unset]):
        ui_messages (Union[List['UiChatItem'], None, Unset]):
        example_input_items (Union[Unset, List['ExampleInputItem']]):
    """

    agent: Union[None, Unset, str] = UNSET
    is_open_agent_rag_view: Union[None, Unset, bool] = UNSET
    thread_id: Union[None, Unset, str] = UNSET
    agent_url_base: Union[None, Unset, str] = UNSET
    graph_image_url: Union[None, Unset, str] = UNSET
    is_dev: Union[None, Unset, bool] = UNSET
    is_open_rag_ui: Union[None, Unset, bool] = UNSET
    is_open_search_view: Union[None, Unset, bool] = UNSET
    is_open_mtm_editor: Union[None, Unset, bool] = UNSET
    uichatitems: Union[List["UIChatMessageItem"], None, Unset] = UNSET
    ui_messages: Union[List["UiChatItem"], None, Unset] = UNSET
    example_input_items: Union[Unset, List["ExampleInputItem"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        agent: Union[None, Unset, str]
        if isinstance(self.agent, Unset):
            agent = UNSET
        else:
            agent = self.agent

        is_open_agent_rag_view: Union[None, Unset, bool]
        if isinstance(self.is_open_agent_rag_view, Unset):
            is_open_agent_rag_view = UNSET
        else:
            is_open_agent_rag_view = self.is_open_agent_rag_view

        thread_id: Union[None, Unset, str]
        if isinstance(self.thread_id, Unset):
            thread_id = UNSET
        else:
            thread_id = self.thread_id

        agent_url_base: Union[None, Unset, str]
        if isinstance(self.agent_url_base, Unset):
            agent_url_base = UNSET
        else:
            agent_url_base = self.agent_url_base

        graph_image_url: Union[None, Unset, str]
        if isinstance(self.graph_image_url, Unset):
            graph_image_url = UNSET
        else:
            graph_image_url = self.graph_image_url

        is_dev: Union[None, Unset, bool]
        if isinstance(self.is_dev, Unset):
            is_dev = UNSET
        else:
            is_dev = self.is_dev

        is_open_rag_ui: Union[None, Unset, bool]
        if isinstance(self.is_open_rag_ui, Unset):
            is_open_rag_ui = UNSET
        else:
            is_open_rag_ui = self.is_open_rag_ui

        is_open_search_view: Union[None, Unset, bool]
        if isinstance(self.is_open_search_view, Unset):
            is_open_search_view = UNSET
        else:
            is_open_search_view = self.is_open_search_view

        is_open_mtm_editor: Union[None, Unset, bool]
        if isinstance(self.is_open_mtm_editor, Unset):
            is_open_mtm_editor = UNSET
        else:
            is_open_mtm_editor = self.is_open_mtm_editor

        uichatitems: Union[List[Dict[str, Any]], None, Unset]
        if isinstance(self.uichatitems, Unset):
            uichatitems = UNSET
        elif isinstance(self.uichatitems, list):
            uichatitems = []
            for uichatitems_type_0_item_data in self.uichatitems:
                uichatitems_type_0_item = uichatitems_type_0_item_data.to_dict()
                uichatitems.append(uichatitems_type_0_item)

        else:
            uichatitems = self.uichatitems

        ui_messages: Union[List[Dict[str, Any]], None, Unset]
        if isinstance(self.ui_messages, Unset):
            ui_messages = UNSET
        elif isinstance(self.ui_messages, list):
            ui_messages = []
            for ui_messages_type_0_item_data in self.ui_messages:
                ui_messages_type_0_item = ui_messages_type_0_item_data.to_dict()
                ui_messages.append(ui_messages_type_0_item)

        else:
            ui_messages = self.ui_messages

        example_input_items: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.example_input_items, Unset):
            example_input_items = []
            for example_input_items_item_data in self.example_input_items:
                example_input_items_item = example_input_items_item_data.to_dict()
                example_input_items.append(example_input_items_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if agent is not UNSET:
            field_dict["agent"] = agent
        if is_open_agent_rag_view is not UNSET:
            field_dict["isOpenAgentRagView"] = is_open_agent_rag_view
        if thread_id is not UNSET:
            field_dict["threadId"] = thread_id
        if agent_url_base is not UNSET:
            field_dict["agent_url_base"] = agent_url_base
        if graph_image_url is not UNSET:
            field_dict["graph_image_url"] = graph_image_url
        if is_dev is not UNSET:
            field_dict["isDev"] = is_dev
        if is_open_rag_ui is not UNSET:
            field_dict["isOpenRagUi"] = is_open_rag_ui
        if is_open_search_view is not UNSET:
            field_dict["isOpenSearchView"] = is_open_search_view
        if is_open_mtm_editor is not UNSET:
            field_dict["isOpenMtmEditor"] = is_open_mtm_editor
        if uichatitems is not UNSET:
            field_dict["uichatitems"] = uichatitems
        if ui_messages is not UNSET:
            field_dict["ui_messages"] = ui_messages
        if example_input_items is not UNSET:
            field_dict["example_input_items"] = example_input_items

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.example_input_item import ExampleInputItem
        from ..models.ui_chat_item import UiChatItem
        from ..models.ui_chat_message_item import UIChatMessageItem

        d = src_dict.copy()

        def _parse_agent(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        agent = _parse_agent(d.pop("agent", UNSET))

        def _parse_is_open_agent_rag_view(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        is_open_agent_rag_view = _parse_is_open_agent_rag_view(d.pop("isOpenAgentRagView", UNSET))

        def _parse_thread_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        thread_id = _parse_thread_id(d.pop("threadId", UNSET))

        def _parse_agent_url_base(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        agent_url_base = _parse_agent_url_base(d.pop("agent_url_base", UNSET))

        def _parse_graph_image_url(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        graph_image_url = _parse_graph_image_url(d.pop("graph_image_url", UNSET))

        def _parse_is_dev(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        is_dev = _parse_is_dev(d.pop("isDev", UNSET))

        def _parse_is_open_rag_ui(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        is_open_rag_ui = _parse_is_open_rag_ui(d.pop("isOpenRagUi", UNSET))

        def _parse_is_open_search_view(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        is_open_search_view = _parse_is_open_search_view(d.pop("isOpenSearchView", UNSET))

        def _parse_is_open_mtm_editor(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        is_open_mtm_editor = _parse_is_open_mtm_editor(d.pop("isOpenMtmEditor", UNSET))

        def _parse_uichatitems(data: object) -> Union[List["UIChatMessageItem"], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                uichatitems_type_0 = []
                _uichatitems_type_0 = data
                for uichatitems_type_0_item_data in _uichatitems_type_0:
                    uichatitems_type_0_item = UIChatMessageItem.from_dict(uichatitems_type_0_item_data)

                    uichatitems_type_0.append(uichatitems_type_0_item)

                return uichatitems_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List["UIChatMessageItem"], None, Unset], data)

        uichatitems = _parse_uichatitems(d.pop("uichatitems", UNSET))

        def _parse_ui_messages(data: object) -> Union[List["UiChatItem"], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                ui_messages_type_0 = []
                _ui_messages_type_0 = data
                for ui_messages_type_0_item_data in _ui_messages_type_0:
                    ui_messages_type_0_item = UiChatItem.from_dict(ui_messages_type_0_item_data)

                    ui_messages_type_0.append(ui_messages_type_0_item)

                return ui_messages_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List["UiChatItem"], None, Unset], data)

        ui_messages = _parse_ui_messages(d.pop("ui_messages", UNSET))

        example_input_items = []
        _example_input_items = d.pop("example_input_items", UNSET)
        for example_input_items_item_data in _example_input_items or []:
            example_input_items_item = ExampleInputItem.from_dict(example_input_items_item_data)

            example_input_items.append(example_input_items_item)

        chat_bot_ui_state = cls(
            agent=agent,
            is_open_agent_rag_view=is_open_agent_rag_view,
            thread_id=thread_id,
            agent_url_base=agent_url_base,
            graph_image_url=graph_image_url,
            is_dev=is_dev,
            is_open_rag_ui=is_open_rag_ui,
            is_open_search_view=is_open_search_view,
            is_open_mtm_editor=is_open_mtm_editor,
            uichatitems=uichatitems,
            ui_messages=ui_messages,
            example_input_items=example_input_items,
        )

        chat_bot_ui_state.additional_properties = d
        return chat_bot_ui_state

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
