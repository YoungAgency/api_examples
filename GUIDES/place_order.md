# Placing an Order (SOR)

Young Platform executes orders via **Smart Order Routing (SOR)**: 
1. you submit a LIMIT order, it's validated and accepted (`202`) synchronously.
2. Matched asynchronously across venues. There is no synchronous fill confirmation — either poll `GET /private/sor/orders/{client_order_id}`, or subscribe to the `SOR.EXECUTIONS` WebSocket topic to receive the outcome pushed as it happens (see [Live updates over WebSocket](#live-updates-over-websocket) below).

See the [OpenAPI reference](../docs/openapi.html) for the full schema (`PlaceSorOrderClient`, `SorOrder`).

## Endpoints

```
POST /api/v1/trader/private/sor/orders                       # place
GET  /api/v1/trader/private/sor/orders/{client_order_id}      # poll status
```

Both use standard [Trader API auth](./auth.md) (`Authorization: Bearer <JWT>` + `X-Api-Key-Id`, `aud: "trader"`, body-bound `hash_payload`). Placing an order additionally requires the API key to have the **trade** permission.

## Request fields (`PlaceSorOrderClient`)

| Field | Required | Notes |
|-------|----------|-------|
| `client_order_id` | **Yes** | Caller-supplied **UUID** — the idempotency key. Retrying with the same value never places a second order; use it to reconcile after a timeout. |
| `market` | Yes | `BASE-QUOTE`, e.g. `BTC-EUR`. |
| `price` | Yes | Limit price, quote currency, decimal string. |
| `quantity` | Yes | Quantity to trade, base currency, decimal string. |
| `side` | Yes | `1` = buy, `2` = sell. |
| `type` | Yes | `1` = LIMIT (the only supported type). |
| `time_in_force` | Yes | `1` = FOK (all-or-nothing) |

## Response (`SorOrder`)

*Status*:

| Value | Status | Terminal | Notes |
|-------|--------|----------|-------|
| `1` | New | No | Accepted, not yet matched. |
| `2` | PartiallyFilled | No | Some quantity matched, routing continues. |
| `3` | Filled | Yes | Fully matched. |
| `4` | Cancelled | Yes | Includes an unmatched FOK/IOC order — expected, not an error. |
| `5` | Expired | Yes | Time-in-force elapsed before matching. |
| `6` | Rejected | Yes | Not accepted for execution. |

An unmatched FOK/IOC order ends up `4` (Cancelled) — that's expected, not an error. `matched_quantity` / `matched_amount` / `fee` fill in as the order executes; `matches` lists individual fills.

## Idempotent retries

> If the place request times out or you're unsure whether it landed, **retry with the same `client_order_id`** — it's the idempotency key, so a retry never double-places.

Then reconcile with `GET /private/sor/orders/{client_order_id}` to see what actually happened.


## Example: place → wait → poll

Mints a fresh trader JWT per request (body-bound, see [auth.md](./auth.md)), places the order, waits 1s for SOR to route it, then fetches the final state by `client_order_id`.

```python
import hashlib, json, os, time, uuid
import jwt        # pip install pyjwt
import requests   # pip install requests

HOST = "https://api.youngplatform.com/api/v1/trader"
KEY_ID = os.environ["YP_KEY_ID"]
PUBLIC_KEY = os.environ["YP_PUBLIC_KEY"]
PRIVATE_KEY = os.environ["YP_PRIVATE_KEY"]


def trader_jwt(body: bytes) -> str:
    iat = int(time.time())
    claims = {
        "sub": PUBLIC_KEY,
        "aud": "trader",
        "iat": iat,
        "exp": iat + 30,       # <= 60s server cap
        "hash_payload": hashlib.sha256(body).hexdigest(),
    }
    return jwt.encode(claims, PRIVATE_KEY, algorithm="HS256")


def auth_headers(body: bytes) -> dict:
    return {
        "Authorization": f"Bearer {trader_jwt(body)}",
        "X-Api-Key-Id": KEY_ID,
        "Content-Type": "application/json",
    }


# 1. Place the order
client_order_id = str(uuid.uuid4())
place_body = json.dumps(
    {
        "client_order_id": client_order_id,
        "market": "BTC-EUR",
        "side": 1,             # 1 = buy
        "type": 1,             # 1 = LIMIT
        "time_in_force": 1,    # 1 = FOK
        "quantity": "0.001",
        "price": "60000",
    }
).encode()

resp = requests.post(f"{HOST}/private/sor/orders", data=place_body, headers=auth_headers(place_body))
resp.raise_for_status()  # 202 Accepted
print("placed:", resp.status_code, resp.json())

# 2. Give SOR a moment to route and match
time.sleep(1)

# 3. Poll the order by its client_order_id to see the outcome
get_resp = requests.get(f"{HOST}/private/sor/orders/{client_order_id}", headers=auth_headers(b""))
get_resp.raise_for_status()
order = get_resp.json()
print("status:", order["status"], "matched_quantity:", order["matched_quantity"])
```

1 second is usually enough to see a terminal status for a marketable IOC/FOK order, but SOR execution is asynchronous — for anything besides a quick manual check, poll on an interval (or with backoff) until `status` is terminal (`3` Filled, `4` Cancelled, `5` Expired, `6` Rejected) rather than assuming one fixed sleep is always enough.


## Live updates over WebSocket

Instead of polling, you can subscribe to the `SOR.EXECUTIONS` topic on the WebSocket API and receive each order update — including matches and the terminal status — pushed to you. The topic is authenticated and scoped to your account; append a market (`SOR.EXECUTIONS.<market>`) to filter to one pair. Its payload mirrors the `SorOrder` fields and enums used above. See the [WebSocket guide](./websocket.md#sorexecutionspair--order-executions-authenticated) for the full payload schema.

A minimal watcher: connect with the same trader JWT (connect/login carries no body, so `hash_payload` is `sha256("")`), subscribe, and print updates until the order reaches a terminal status. Run with `uv run --with websockets --with pyjwt watch_order.py`.

```python
import asyncio, hashlib, json, os, time
import jwt        # pip install pyjwt
import websockets # pip install websockets

WS_URL = "wss://api.youngplatform.com/api/socket/ws"
MARKET = "BTC-EUR"
TERMINAL = {3, 4, 5, 6}  # Filled, Cancelled, Expired, Rejected


def trader_jwt() -> str:
    iat = int(time.time())
    claims = {
        "sub": os.environ["YP_PUBLIC_KEY"],
        "aud": "trader",
        "iat": iat,
        "exp": iat + 30,  # <= 60s server cap
        "hash_payload": hashlib.sha256(b"").hexdigest(),
    }
    return jwt.encode(claims, os.environ["YP_PRIVATE_KEY"], algorithm="HS256")


async def main() -> None:
    headers = {
        "Authorization": f"Bearer {trader_jwt()}",
        "X-Api-Key-Id": os.environ["YP_KEY_ID"],
    }
    async with websockets.connect(WS_URL, additional_headers=headers) as ws:
        await ws.send(json.dumps({
            "id": "1",
            "method": "subscribe",
            "events": [f"SOR.EXECUTIONS.{MARKET}"],
        }))
        async for raw in ws:
            msg = json.loads(raw)
            if msg.get("type") != f"SOR.EXECUTIONS.{MARKET}":
                continue  # skip login/subscribe acks
            for order in msg["data"]:
                print("status:", order["status"], "matches:", order.get("matches", []))
                if order["status"] in TERMINAL:
                    return

asyncio.run(main())
```

Subscribe *before* (or right after) placing the order so you don't miss a fast terminal update. For a quick manual check the REST poll above is simpler; the WebSocket subscription is the better fit when you're tracking many orders or want push updates without a poll loop.

## See also

- [API Key Authentication](./auth.md) — credentials, JWT claims, `hash_payload`.
- [WebSocket API](./websocket.md) — real-time market data and order/balance updates.
- [OpenAPI reference](../docs/openapi.html) — full request/response schemas.
