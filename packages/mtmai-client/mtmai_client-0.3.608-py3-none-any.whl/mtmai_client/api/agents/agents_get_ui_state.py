from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.chat_bot_ui_state_public import ChatBotUiStatePublic
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    agent_id: str,
    thread_id: str,
) -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/api/v1/agents/{agent_id}/{thread_id}/uistate",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ChatBotUiStatePublic, HTTPValidationError]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ChatBotUiStatePublic.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[ChatBotUiStatePublic, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    agent_id: str,
    thread_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[ChatBotUiStatePublic, HTTPValidationError]]:
    """获取 chat bot UiState

    Args:
        agent_id (str):
        thread_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ChatBotUiStatePublic, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        agent_id=agent_id,
        thread_id=thread_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    agent_id: str,
    thread_id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[ChatBotUiStatePublic, HTTPValidationError]]:
    """获取 chat bot UiState

    Args:
        agent_id (str):
        thread_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ChatBotUiStatePublic, HTTPValidationError]
    """

    return sync_detailed(
        agent_id=agent_id,
        thread_id=thread_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    agent_id: str,
    thread_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[ChatBotUiStatePublic, HTTPValidationError]]:
    """获取 chat bot UiState

    Args:
        agent_id (str):
        thread_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ChatBotUiStatePublic, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        agent_id=agent_id,
        thread_id=thread_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    agent_id: str,
    thread_id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[ChatBotUiStatePublic, HTTPValidationError]]:
    """获取 chat bot UiState

    Args:
        agent_id (str):
        thread_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ChatBotUiStatePublic, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            agent_id=agent_id,
            thread_id=thread_id,
            client=client,
        )
    ).parsed
