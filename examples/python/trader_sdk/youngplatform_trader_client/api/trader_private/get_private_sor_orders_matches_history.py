from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.sor_match_page import SorMatchPage
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    market: str | Unset = UNSET,
    before: str | Unset = UNSET,
    before_id: int | Unset = UNSET,
    limit: int | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["market"] = market

    params["before"] = before

    params["before_id"] = before_id

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/private/sor/orders/matches/history",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | SorMatchPage | None:
    if response.status_code == 200:
        response_200 = SorMatchPage.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = ErrorResponse.from_dict(response.json())

        return response_401

    if response.status_code == 500:
        response_500 = ErrorResponse.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | SorMatchPage]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    market: str | Unset = UNSET,
    before: str | Unset = UNSET,
    before_id: int | Unset = UNSET,
    limit: int | Unset = UNSET,
) -> Response[ErrorResponse | SorMatchPage]:
    """List historical SOR matches

     Retrieve the authenticated customer's individual SOR fills (matches) across all their orders, most
    recent first, with keyset pagination: while has_more is true, pass next_cursor.timestamp as before
    and next_cursor.id as before_id to fetch the next page (limit is capped at 100). Each match
    references its parent order by client_order_id and carries the market, venue, executed
    quantity/price/amount and venue fee. Authenticated via API key.

    Args:
        market (str | Unset):
        before (str | Unset):
        before_id (int | Unset):
        limit (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | SorMatchPage]
    """

    kwargs = _get_kwargs(
        market=market,
        before=before,
        before_id=before_id,
        limit=limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    market: str | Unset = UNSET,
    before: str | Unset = UNSET,
    before_id: int | Unset = UNSET,
    limit: int | Unset = UNSET,
) -> ErrorResponse | SorMatchPage | None:
    """List historical SOR matches

     Retrieve the authenticated customer's individual SOR fills (matches) across all their orders, most
    recent first, with keyset pagination: while has_more is true, pass next_cursor.timestamp as before
    and next_cursor.id as before_id to fetch the next page (limit is capped at 100). Each match
    references its parent order by client_order_id and carries the market, venue, executed
    quantity/price/amount and venue fee. Authenticated via API key.

    Args:
        market (str | Unset):
        before (str | Unset):
        before_id (int | Unset):
        limit (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | SorMatchPage
    """

    return sync_detailed(
        client=client,
        market=market,
        before=before,
        before_id=before_id,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    market: str | Unset = UNSET,
    before: str | Unset = UNSET,
    before_id: int | Unset = UNSET,
    limit: int | Unset = UNSET,
) -> Response[ErrorResponse | SorMatchPage]:
    """List historical SOR matches

     Retrieve the authenticated customer's individual SOR fills (matches) across all their orders, most
    recent first, with keyset pagination: while has_more is true, pass next_cursor.timestamp as before
    and next_cursor.id as before_id to fetch the next page (limit is capped at 100). Each match
    references its parent order by client_order_id and carries the market, venue, executed
    quantity/price/amount and venue fee. Authenticated via API key.

    Args:
        market (str | Unset):
        before (str | Unset):
        before_id (int | Unset):
        limit (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | SorMatchPage]
    """

    kwargs = _get_kwargs(
        market=market,
        before=before,
        before_id=before_id,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    market: str | Unset = UNSET,
    before: str | Unset = UNSET,
    before_id: int | Unset = UNSET,
    limit: int | Unset = UNSET,
) -> ErrorResponse | SorMatchPage | None:
    """List historical SOR matches

     Retrieve the authenticated customer's individual SOR fills (matches) across all their orders, most
    recent first, with keyset pagination: while has_more is true, pass next_cursor.timestamp as before
    and next_cursor.id as before_id to fetch the next page (limit is capped at 100). Each match
    references its parent order by client_order_id and carries the market, venue, executed
    quantity/price/amount and venue fee. Authenticated via API key.

    Args:
        market (str | Unset):
        before (str | Unset):
        before_id (int | Unset):
        limit (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | SorMatchPage
    """

    return (
        await asyncio_detailed(
            client=client,
            market=market,
            before=before,
            before_id=before_id,
            limit=limit,
        )
    ).parsed
