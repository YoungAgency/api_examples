# Python SDK

A typed Python client for the Young Platform **trader API**, generated directly from the [OpenAPI reference](../docs/openapi.html). It gives you a function per endpoint, `attrs` models for every request and response, and per-request JWT auth wired in — so you call the API in Python without hand-writing HTTP requests, headers, or token minting.

The full project lives at [examples/python/trader_sdk/](https://github.com/YoungAgency/youngplatform_api_docs/tree/main/examples/python/trader_sdk) — a runnable [uv](https://docs.astral.sh/uv/) project you can clone and use as a starting point.

## What's in the box

```
pyproject.toml               uv project (httpx, attrs, pyjwt)
youngplatform_trader_client/ the generated SDK — a function per endpoint + attrs models
young_auth.py                httpx.Auth that mints a fresh, body-bound trader JWT per request
app.py                       runnable tester — exercises every read endpoint and prints results
generate_sdk.sh              regenerates the client from ../../../trader_openapi.json
```

- **[youngplatform_trader_client/](https://github.com/YoungAgency/youngplatform_api_docs/tree/main/examples/python/trader_sdk/youngplatform_trader_client)** — the generated client. Endpoints are grouped by surface into `api.trader_public` and `api.trader_private`; every request/response body has a matching model under `models`. **Generated — don't edit by hand.**
- **[young_auth.py](https://github.com/YoungAgency/youngplatform_api_docs/blob/main/examples/python/trader_sdk/young_auth.py)** — a small `httpx.Auth` (`TraderAuth`) that hashes each request body and sets both the `Authorization: Bearer <JWT>` and `X-Api-Key-Id` headers, minting a fresh token per request. This is what keeps auth correct as bodies change (see [API Key Authentication](./auth.md)).
- **[app.py](https://github.com/YoungAgency/youngplatform_api_docs/blob/main/examples/python/trader_sdk/app.py)** — a tester that wires the client to `TraderAuth` and calls each endpoint. The best place to see the SDK in use end-to-end.

## Setup

```bash
uv sync    # creates .venv and installs dependencies
```

Generate an API key at pro.youngplatform.com and export your credentials — nothing is hard-coded (see [API Key Authentication](./auth.md) for what each value is):

```bash
export YP_KEY_ID=...       # X-Api-Key-Id header
export YP_PUBLIC_KEY=...   # JWT "sub" — your enrolled public identifier
export YP_PRIVATE_KEY=...  # HS256 signing secret
export YP_API_HOST=https://api.youngplatform.com   # optional; this is the default
```

## Run the tester

```bash
uv run app.py                    # markets, ticker, liquidity, charts, balance, profile, SOR history
uv run app.py --market ETH-EUR   # override the market for per-market endpoints
```

Each call prints its HTTP status and parsed body. Auth failures (401/403) are printed, not raised, so one failing endpoint doesn't stop the run.

## Using the client

Build an `AuthenticatedClient` pointed at the trader base path and hand it `TraderAuth` as the httpx `auth`; from then on you just call endpoint functions with typed models. This is the same wiring `app.py` uses:

```python
import os
from youngplatform_trader_client import AuthenticatedClient
from youngplatform_trader_client.api.trader_public import get_public_markets
from youngplatform_trader_client.api.trader_private import get_private_balance
from young_auth import TraderAuth

client = AuthenticatedClient(
    base_url=os.environ.get("YP_API_HOST", "https://api.youngplatform.com") + "/api/v1/trader",
    token="unused",  # placeholder; TraderAuth sets the real Authorization header per request
    raise_on_unexpected_status=False,
    httpx_args={"auth": TraderAuth(
        os.environ["YP_KEY_ID"],
        os.environ["YP_PUBLIC_KEY"],
        os.environ["YP_PRIVATE_KEY"],
    )},
)

with client as c:
    markets = get_public_markets.sync_detailed(client=c)   # public — no credentials needed
    balance = get_private_balance.sync_detailed(client=c)  # private — authenticated by TraderAuth
    print(markets.status_code, balance.parsed)
```

Each endpoint function offers `sync_detailed` / `asyncio_detailed` (returning a `Response` with `status_code`, `parsed`, and raw `content`) and `sync` / `asyncio` (returning just the parsed body). The `.parsed` value is a typed model instance — call `.to_dict()` to get plain JSON.

### Placing an order

Write endpoints take a typed request model. Placing a SOR order uses `PlaceSorOrderClient` with enum values for side, type, and time-in-force:

```python
import uuid
from youngplatform_trader_client.api.trader_private import post_private_sor_orders
from youngplatform_trader_client.models import PlaceSorOrderClient, Side, SorOrderType, SorTimeInForce

body = PlaceSorOrderClient(
    market="BTC-EUR",
    side=Side.SIDE_BUY,
    type_=SorOrderType.SOR_ORDER_TYPE_LIMIT,
    time_in_force=SorTimeInForce.SOR_TIME_IN_FORCE_FOK,
    price="98750.00",
    quantity="0.01",
    client_order_id=str(uuid.uuid4()),  # required UUID idempotency key
)
resp = post_private_sor_orders.sync_detailed(client=c, body=body)
```

See [Placing an Order (SOR)](./place_order.md) for the full place → wait → poll flow and the semantics of `client_order_id`.

## Regenerating the SDK

`youngplatform_trader_client/` is generated by [openapi-python-client](https://github.com/openapi-generators/openapi-python-client) from `trader_openapi.json`. When the spec changes, regenerate rather than editing the client:

```bash
./generate_sdk.sh
```

## See also

- [API Key Authentication](./auth.md) — the JWT claims and `hash_payload` that `TraderAuth` implements.
- [Placing an Order (SOR)](./place_order.md) — full POST request/response schema and place → wait → poll example.
- [WebSocket API](./websocket.md) — live market data and account streams.
- [OpenAPI reference](../docs/openapi.html) — the spec the SDK is generated from.
- Project source: [examples/python/trader_sdk/](https://github.com/YoungAgency/youngplatform_api_docs/tree/main/examples/python/trader_sdk).
