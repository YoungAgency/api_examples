from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.trader_charts import TraderCharts
from ...types import UNSET, Response, Unset


def _get_kwargs(
    market: str,
    *,
    interval: int | Unset = 1440,
    limit: int | Unset = 100,
    to: str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["interval"] = interval

    params["limit"] = limit

    params["to"] = to

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/public/charts/{market}".format(
            market=quote(str(market), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | TraderCharts | None:
    if response.status_code == 200:
        response_200 = TraderCharts.from_dict(response.json())

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
) -> Response[ErrorResponse | TraderCharts]:
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
    interval: int | Unset = 1440,
    limit: int | Unset = 100,
    to: str | Unset = UNSET,
) -> Response[ErrorResponse | TraderCharts]:
    """Get OHLC charts

     Retrieve historical OHLC candles for a market, most recent first. interval is the candle size in
    minutes (1, 5, 15, 60, 240, 1440); to is the upper bound of the window as an ISO-8601 date-time
    (omit for the latest) and is inclusive of a candle's open_at — to paginate backwards, pass a
    timestamp just before the oldest returned open_at. Volume/amount fields are not populated yet. No
    authentication required.

    Args:
        market (str):
        interval (int | Unset):  Default: 1440.
        limit (int | Unset):  Default: 100.
        to (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | TraderCharts]
    """

    kwargs = _get_kwargs(
        market=market,
        interval=interval,
        limit=limit,
        to=to,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    market: str,
    *,
    client: AuthenticatedClient | Client,
    interval: int | Unset = 1440,
    limit: int | Unset = 100,
    to: str | Unset = UNSET,
) -> ErrorResponse | TraderCharts | None:
    """Get OHLC charts

     Retrieve historical OHLC candles for a market, most recent first. interval is the candle size in
    minutes (1, 5, 15, 60, 240, 1440); to is the upper bound of the window as an ISO-8601 date-time
    (omit for the latest) and is inclusive of a candle's open_at — to paginate backwards, pass a
    timestamp just before the oldest returned open_at. Volume/amount fields are not populated yet. No
    authentication required.

    Args:
        market (str):
        interval (int | Unset):  Default: 1440.
        limit (int | Unset):  Default: 100.
        to (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | TraderCharts
    """

    return sync_detailed(
        market=market,
        client=client,
        interval=interval,
        limit=limit,
        to=to,
    ).parsed


async def asyncio_detailed(
    market: str,
    *,
    client: AuthenticatedClient | Client,
    interval: int | Unset = 1440,
    limit: int | Unset = 100,
    to: str | Unset = UNSET,
) -> Response[ErrorResponse | TraderCharts]:
    """Get OHLC charts

     Retrieve historical OHLC candles for a market, most recent first. interval is the candle size in
    minutes (1, 5, 15, 60, 240, 1440); to is the upper bound of the window as an ISO-8601 date-time
    (omit for the latest) and is inclusive of a candle's open_at — to paginate backwards, pass a
    timestamp just before the oldest returned open_at. Volume/amount fields are not populated yet. No
    authentication required.

    Args:
        market (str):
        interval (int | Unset):  Default: 1440.
        limit (int | Unset):  Default: 100.
        to (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | TraderCharts]
    """

    kwargs = _get_kwargs(
        market=market,
        interval=interval,
        limit=limit,
        to=to,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    market: str,
    *,
    client: AuthenticatedClient | Client,
    interval: int | Unset = 1440,
    limit: int | Unset = 100,
    to: str | Unset = UNSET,
) -> ErrorResponse | TraderCharts | None:
    """Get OHLC charts

     Retrieve historical OHLC candles for a market, most recent first. interval is the candle size in
    minutes (1, 5, 15, 60, 240, 1440); to is the upper bound of the window as an ISO-8601 date-time
    (omit for the latest) and is inclusive of a candle's open_at — to paginate backwards, pass a
    timestamp just before the oldest returned open_at. Volume/amount fields are not populated yet. No
    authentication required.

    Args:
        market (str):
        interval (int | Unset):  Default: 1440.
        limit (int | Unset):  Default: 100.
        to (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | TraderCharts
    """

    return (
        await asyncio_detailed(
            market=market,
            client=client,
            interval=interval,
            limit=limit,
            to=to,
        )
    ).parsed
