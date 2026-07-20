"""Tester for the YoungPlatform trader API using the generated SDK.

Reads credentials and the target host from the environment, then exercises each
read endpoint of the trader API and prints the result. Credentials are never
hard-coded — generate an API key at pro.youngplatform.com and export:

    export YP_KEY_ID=...        # X-Api-Key-Id header
    export YP_PUBLIC_KEY=...    # JWT "sub" (enrolled public identifier)
    export YP_PRIVATE_KEY=...   # HS256 signing secret
    export YP_API_HOST=https://api.youngplatform.com   # optional, this is the default

Run with:

    uv run app.py
    uv run app.py --market BTC-EUR
"""

from __future__ import annotations

import argparse
import os
import sys
import uuid
import json
import time
from http import HTTPStatus
from typing import Any, Callable

from youngplatform_trader_client import AuthenticatedClient
from youngplatform_trader_client.api.trader_private import (
    get_private_balance,
    get_private_profile,
    get_private_sor_history,
    get_private_sor_orders_client_order_id,
    post_private_sor_orders,
)
from youngplatform_trader_client.api.trader_public import (
    get_public_charts_market,
    get_public_liquidity_market,
    get_public_markets,
    get_public_tickers,
    get_public_tickers_market,
)
from youngplatform_trader_client.models import (
    PlaceSorOrderClient,
    Side,
    SorOrderType,
    SorTimeInForce,
)
from youngplatform_trader_client.types import Response
from young_auth import TraderAuth

DEFAULT_HOST = "https://api.youngplatform.com"
# The trader API is versioned under /api/v1/trader; endpoint paths are relative to
# it (/public/... for market data, /private/... for account-scoped requests).
API_BASE_PATH = "/api/v1/trader"


def build_client() -> AuthenticatedClient:
    """Construct an SDK client wired to mint a fresh trader JWT per request."""
    key_id = os.environ.get("YP_KEY_ID")
    public_key = os.environ.get("YP_PUBLIC_KEY")
    private_key = os.environ.get("YP_PRIVATE_KEY")
    host = os.environ.get("YP_API_HOST", DEFAULT_HOST).rstrip("/")

    missing = [
        name
        for name, value in (
            ("YP_KEY_ID", key_id),
            ("YP_PUBLIC_KEY", public_key),
            ("YP_PRIVATE_KEY", private_key),
        )
        if not value
    ]
    if missing:
        raise SystemExit(f"Missing required env vars: {', '.join(missing)}")

    return AuthenticatedClient(
        base_url=host + API_BASE_PATH,
        # token is unused: TraderAuth mints and sets the Authorization header per
        # request, overriding this placeholder. It only satisfies the SDK's
        # AuthenticatedClient contract (some endpoints require it).
        token="unused",
        raise_on_unexpected_status=False,
        httpx_args={
            "auth": TraderAuth(key_id, public_key, private_key),  # type: ignore[arg-type]
        },
    )


def show(label: str, call: Callable[[], Response[Any]]) -> None:
    """Run one endpoint call and print its status + parsed body (or error)."""
    print(f"\n=== {label} ===")
    try:
        response = call()
    except Exception as exc:  # network/timeout/etc — keep the tester going
        print(f"  request failed: {exc!r}")
        return

    status = HTTPStatus(response.status_code)
    print(f"  HTTP {status.value} {status.phrase}")
    if response.parsed is not None:
        print(f"  {json.dumps(response.parsed.to_dict(), indent=2)}")
        print(f"  {response.parsed}")
    elif response.content:
        # Undocumented status (e.g. 401/403) — show the raw body.
        print(f"  body: {response.content.decode(errors='replace')}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--market",
        default="BTC-EUR",
        help="market symbol for per-market endpoints (default: BTC-EUR)",
    )
    parser.add_argument(
        "--place-order",
        action="store_true",
        help="ALSO place a real FOK LIMIT SOR order (MOVES REAL FUNDS), then "
        "fetch it back by client_order_id. Requires --price and --quantity.",
    )
    parser.add_argument("--side", choices=["buy", "sell"], default="buy")
    parser.add_argument("--price", help="limit price (quote currency)")
    parser.add_argument("--quantity", help="order quantity (base currency)")
    args = parser.parse_args()

    client = build_client()
    with client as c:
        # Public market data (unauthenticated on the server; the minted JWT is
        # simply ignored by the /public group).
        show("GET /public/markets", lambda: get_public_markets.sync_detailed(client=c))
        show("GET /public/tickers", lambda: get_public_tickers.sync_detailed(client=c))
        show(
            f"GET /public/tickers/{args.market}",
            lambda: get_public_tickers_market.sync_detailed(args.market, client=c),
        )
        show(
            f"GET /public/liquidity/{args.market}",
            lambda: get_public_liquidity_market.sync_detailed(args.market, client=c),
        )
        show(
            f"GET /public/charts/{args.market}",
            lambda: get_public_charts_market.sync_detailed(
                args.market, client=c, interval=1440, limit=5
            ),
        )
        # Private, account-scoped.
        show("GET /private/balance", lambda: get_private_balance.sync_detailed(client=c))
        show("GET /private/profile", lambda: get_private_profile.sync_detailed(client=c))
        show(
            "GET /private/sor/history",
            lambda: get_private_sor_history.sync_detailed(
                client=c, limit=5, with_trades=True
            ),
        )

        if args.place_order:
            place_and_fetch_order(c, args)
    return 0


def place_and_fetch_order(c: AuthenticatedClient, args: argparse.Namespace) -> None:
    """Opt-in demo of the write surface: place a FOK LIMIT order, then read it
    back by its client_order_id. Guarded by --place-order because it moves real
    funds."""
    if not args.price or not args.quantity:
        print("\n--place-order requires --price and --quantity; skipping.")
        return

    # client_order_id is REQUIRED on the trader API and must be a UUID: it is the
    # idempotency key, generated up-front so the order can be reconciled via
    # GET /private/sor/orders/{client_order_id} even if the POST times out.
    coid = str(uuid.uuid4())
    body = PlaceSorOrderClient(
        market=args.market,
        side=Side.SIDE_BUY if args.side == "buy" else Side.SIDE_SELL,
        type_=SorOrderType.SOR_ORDER_TYPE_LIMIT,
        time_in_force=SorTimeInForce.SOR_TIME_IN_FORCE_FOK,
        price=args.price,
        quantity=args.quantity,
        client_order_id=coid,
    )

    # Place exactly once, then read it back by the client_order_id we chose.
    print(f"\n=== POST /private/sor/orders (client_order_id={coid}) ===")
    response = post_private_sor_orders.sync_detailed(client=c, body=body)
    status = HTTPStatus(response.status_code)
    print(f"  HTTP {status.value} {status.phrase}")
    if response.parsed is not None:
        print(f"  {json.dumps(response.parsed.to_dict(), indent=2)}")
    elif response.content:
        print(f"  body: {response.content.decode(errors='replace')}")

    time.sleep(2)  # give the server a moment to reconcile the order before we fetch it
    show(
        f"GET /private/sor/orders/{coid}",
        lambda: get_private_sor_orders_client_order_id.sync_detailed(coid, client=c),
    )


if __name__ == "__main__":
    sys.exit(main())
