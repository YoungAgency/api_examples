from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.ticker import Ticker
from ...types import Response


def _get_kwargs(
    market: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/public/tickers/{market}".format(
            market=quote(str(market), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | Ticker | None:
    if response.status_code == 200:
        response_200 = Ticker.from_dict(response.json())

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
) -> Response[ErrorResponse | Ticker]:
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
) -> Response[ErrorResponse | Ticker]:
    """Get ticker

     Retrieve the rolling OHLC ticker snapshot for a single market. Note the compact field keys
    (mkt/o/h/l/c/qty/amt/t); t is epoch milliseconds. No authentication required.

    Args:
        market (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | Ticker]
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
) -> ErrorResponse | Ticker | None:
    """Get ticker

     Retrieve the rolling OHLC ticker snapshot for a single market. Note the compact field keys
    (mkt/o/h/l/c/qty/amt/t); t is epoch milliseconds. No authentication required.

    Args:
        market (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | Ticker
    """

    return sync_detailed(
        market=market,
        client=client,
    ).parsed


async def asyncio_detailed(
    market: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ErrorResponse | Ticker]:
    """Get ticker

     Retrieve the rolling OHLC ticker snapshot for a single market. Note the compact field keys
    (mkt/o/h/l/c/qty/amt/t); t is epoch milliseconds. No authentication required.

    Args:
        market (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | Ticker]
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
) -> ErrorResponse | Ticker | None:
    """Get ticker

     Retrieve the rolling OHLC ticker snapshot for a single market. Note the compact field keys
    (mkt/o/h/l/c/qty/amt/t); t is epoch milliseconds. No authentication required.

    Args:
        market (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | Ticker
    """

    return (
        await asyncio_detailed(
            market=market,
            client=client,
        )
    ).parsed
