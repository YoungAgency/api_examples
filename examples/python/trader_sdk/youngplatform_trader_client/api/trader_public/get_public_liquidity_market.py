from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.trader_book_response import TraderBookResponse
from ...types import Response


def _get_kwargs(
    market: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/public/liquidity/{market}".format(
            market=quote(str(market), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | TraderBookResponse | None:
    if response.status_code == 200:
        response_200 = TraderBookResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | TraderBookResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    market: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ErrorResponse | TraderBookResponse]:
    """Get aggregated liquidity

     Retrieve the liquidity currently available for a market as price levels (bids/asks) plus a mid
    price. This is indicative liquidity aggregated across sources — not the order book of a single
    trading venue — so it should be treated as an estimate of executable depth. No authentication
    required.

    Args:
        market (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | TraderBookResponse]
    """

    kwargs = _get_kwargs(
        market=market,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    market: str,
    *,
    client: AuthenticatedClient | Client,
) -> ErrorResponse | TraderBookResponse | None:
    """Get aggregated liquidity

     Retrieve the liquidity currently available for a market as price levels (bids/asks) plus a mid
    price. This is indicative liquidity aggregated across sources — not the order book of a single
    trading venue — so it should be treated as an estimate of executable depth. No authentication
    required.

    Args:
        market (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | TraderBookResponse
    """

    return sync_detailed(
        market=market,
        client=client,
    ).parsed


async def asyncio_detailed(
    market: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ErrorResponse | TraderBookResponse]:
    """Get aggregated liquidity

     Retrieve the liquidity currently available for a market as price levels (bids/asks) plus a mid
    price. This is indicative liquidity aggregated across sources — not the order book of a single
    trading venue — so it should be treated as an estimate of executable depth. No authentication
    required.

    Args:
        market (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | TraderBookResponse]
    """

    kwargs = _get_kwargs(
        market=market,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    market: str,
    *,
    client: AuthenticatedClient | Client,
) -> ErrorResponse | TraderBookResponse | None:
    """Get aggregated liquidity

     Retrieve the liquidity currently available for a market as price levels (bids/asks) plus a mid
    price. This is indicative liquidity aggregated across sources — not the order book of a single
    trading venue — so it should be treated as an estimate of executable depth. No authentication
    required.

    Args:
        market (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | TraderBookResponse
    """

    return (
        await asyncio_detailed(
            market=market,
            client=client,
        )
    ).parsed
