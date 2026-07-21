from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.place_sor_order_client import PlaceSorOrderClient
from ...models.sor_order import SorOrder
from ...types import Response


def _get_kwargs(
    *,
    body: PlaceSorOrderClient,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/private/sor/orders",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | SorOrder | None:
    if response.status_code == 202:
        response_202 = SorOrder.from_dict(response.json())

        return response_202

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
) -> Response[ErrorResponse | SorOrder]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: PlaceSorOrderClient,
) -> Response[ErrorResponse | SorOrder]:
    """Place a SOR order

     Submit a LIMIT order for execution via Smart Order Routing (SOR). The request is accepted (202) once
    the order is validated, the debited balance is locked and the order is persisted; execution then
    happens asynchronously — poll GET /private/sor/orders/{client_order_id} for the outcome. side is 1
    (buy) or 2 (sell); type is 1 (LIMIT, the only supported type); time_in_force is 1 (FOK, all-or-
    nothing) or 2 (IOC, partial fills allowed, remainder cancelled). quantity and price are decimal
    strings in base and quote currency respectively. client_order_id is REQUIRED and must be a UUID: it
    is the idempotency key, so you can safely retry a timed-out request with the same value and
    reconcile the order afterwards. Authenticated via API key with the TRADE permission.

    Args:
        body (PlaceSorOrderClient):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | SorOrder]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: PlaceSorOrderClient,
) -> ErrorResponse | SorOrder | None:
    """Place a SOR order

     Submit a LIMIT order for execution via Smart Order Routing (SOR). The request is accepted (202) once
    the order is validated, the debited balance is locked and the order is persisted; execution then
    happens asynchronously — poll GET /private/sor/orders/{client_order_id} for the outcome. side is 1
    (buy) or 2 (sell); type is 1 (LIMIT, the only supported type); time_in_force is 1 (FOK, all-or-
    nothing) or 2 (IOC, partial fills allowed, remainder cancelled). quantity and price are decimal
    strings in base and quote currency respectively. client_order_id is REQUIRED and must be a UUID: it
    is the idempotency key, so you can safely retry a timed-out request with the same value and
    reconcile the order afterwards. Authenticated via API key with the TRADE permission.

    Args:
        body (PlaceSorOrderClient):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | SorOrder
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: PlaceSorOrderClient,
) -> Response[ErrorResponse | SorOrder]:
    """Place a SOR order

     Submit a LIMIT order for execution via Smart Order Routing (SOR). The request is accepted (202) once
    the order is validated, the debited balance is locked and the order is persisted; execution then
    happens asynchronously — poll GET /private/sor/orders/{client_order_id} for the outcome. side is 1
    (buy) or 2 (sell); type is 1 (LIMIT, the only supported type); time_in_force is 1 (FOK, all-or-
    nothing) or 2 (IOC, partial fills allowed, remainder cancelled). quantity and price are decimal
    strings in base and quote currency respectively. client_order_id is REQUIRED and must be a UUID: it
    is the idempotency key, so you can safely retry a timed-out request with the same value and
    reconcile the order afterwards. Authenticated via API key with the TRADE permission.

    Args:
        body (PlaceSorOrderClient):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | SorOrder]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: PlaceSorOrderClient,
) -> ErrorResponse | SorOrder | None:
    """Place a SOR order

     Submit a LIMIT order for execution via Smart Order Routing (SOR). The request is accepted (202) once
    the order is validated, the debited balance is locked and the order is persisted; execution then
    happens asynchronously — poll GET /private/sor/orders/{client_order_id} for the outcome. side is 1
    (buy) or 2 (sell); type is 1 (LIMIT, the only supported type); time_in_force is 1 (FOK, all-or-
    nothing) or 2 (IOC, partial fills allowed, remainder cancelled). quantity and price are decimal
    strings in base and quote currency respectively. client_order_id is REQUIRED and must be a UUID: it
    is the idempotency key, so you can safely retry a timed-out request with the same value and
    reconcile the order afterwards. Authenticated via API key with the TRADE permission.

    Args:
        body (PlaceSorOrderClient):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | SorOrder
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
