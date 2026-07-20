from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.sor_order import SorOrder
from ...types import Response


def _get_kwargs(
    client_order_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/private/sor/orders/{client_order_id}".format(
            client_order_id=quote(str(client_order_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | SorOrder | None:
    if response.status_code == 200:
        response_200 = SorOrder.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = ErrorResponse.from_dict(response.json())

        return response_401

    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404

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
    client_order_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[ErrorResponse | SorOrder]:
    """Get a SOR order by client order ID

     Retrieve the current state of a SOR order placed by the authenticated customer, including matched
    quantity/amount, fee and per-venue matches once executed. status is 1 (New), 2 (PartiallyFilled), 3
    (Filled), 4 (Cancelled), 5 (Expired) or 6 (Rejected); an unmatched FOK/IOC order ends up Cancelled.
    Poll this endpoint after placing an order (or after a placement timeout, using the same
    client_order_id) to reconcile the outcome. Returns 404 if the order does not exist or belongs to a
    different customer. Authenticated via API key.

    Args:
        client_order_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | SorOrder]
    """

    kwargs = _get_kwargs(
        client_order_id=client_order_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    client_order_id: str,
    *,
    client: AuthenticatedClient,
) -> ErrorResponse | SorOrder | None:
    """Get a SOR order by client order ID

     Retrieve the current state of a SOR order placed by the authenticated customer, including matched
    quantity/amount, fee and per-venue matches once executed. status is 1 (New), 2 (PartiallyFilled), 3
    (Filled), 4 (Cancelled), 5 (Expired) or 6 (Rejected); an unmatched FOK/IOC order ends up Cancelled.
    Poll this endpoint after placing an order (or after a placement timeout, using the same
    client_order_id) to reconcile the outcome. Returns 404 if the order does not exist or belongs to a
    different customer. Authenticated via API key.

    Args:
        client_order_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | SorOrder
    """

    return sync_detailed(
        client_order_id=client_order_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    client_order_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[ErrorResponse | SorOrder]:
    """Get a SOR order by client order ID

     Retrieve the current state of a SOR order placed by the authenticated customer, including matched
    quantity/amount, fee and per-venue matches once executed. status is 1 (New), 2 (PartiallyFilled), 3
    (Filled), 4 (Cancelled), 5 (Expired) or 6 (Rejected); an unmatched FOK/IOC order ends up Cancelled.
    Poll this endpoint after placing an order (or after a placement timeout, using the same
    client_order_id) to reconcile the outcome. Returns 404 if the order does not exist or belongs to a
    different customer. Authenticated via API key.

    Args:
        client_order_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | SorOrder]
    """

    kwargs = _get_kwargs(
        client_order_id=client_order_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    client_order_id: str,
    *,
    client: AuthenticatedClient,
) -> ErrorResponse | SorOrder | None:
    """Get a SOR order by client order ID

     Retrieve the current state of a SOR order placed by the authenticated customer, including matched
    quantity/amount, fee and per-venue matches once executed. status is 1 (New), 2 (PartiallyFilled), 3
    (Filled), 4 (Cancelled), 5 (Expired) or 6 (Rejected); an unmatched FOK/IOC order ends up Cancelled.
    Poll this endpoint after placing an order (or after a placement timeout, using the same
    client_order_id) to reconcile the outcome. Returns 404 if the order does not exist or belongs to a
    different customer. Authenticated via API key.

    Args:
        client_order_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | SorOrder
    """

    return (
        await asyncio_detailed(
            client_order_id=client_order_id,
            client=client,
        )
    ).parsed
