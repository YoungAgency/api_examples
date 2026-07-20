# WebSocket API

Real-time market data and account updates over a single WebSocket connection.

**Endpoint**: `https://api.youngplatform.com/api/socket/ws`


## Connection & authentication

Authentication is **optional at connection time** — you can connect anonymously and subscribe to public topics (`SOR.*`) immediately. Authenticated topics such as `LEDGER` require credentials.

The WebSocket credential is the same short-lived **trader** JWT used for REST (`aud: "trader"`, HS256, signed with your API key).

Because the connection/login carries no body, `hash_payload` is `sha256("")`. See the [Authentication guide](./auth.md) for the full claim set and ready-to-run token minters.

Pass credentials one of two ways.

**1. HTTP headers at connect time:**

```
Authorization: Bearer <access_token>
X-Api-Key-Id: <api_key_id>   (optional — only for API-key-based auth)
```

**2. A `login` message after connecting:**

```json
{ "id": "1", "method": "login", "token": "<access_token>", "keyID": "<api_key_id>" }
```

Response:

```json
{ "id": "1", "type": "login", "message": "ok" }
```

## Message format

Every **client** message:

```json
{
  "id":     "optional-correlation-id",
  "method": "subscribe | unsubscribe | ping | logout | login",
  "events": ["TOPIC.1", "TOPIC.2"]
}
```

Every **server** message:

```json
{
  "id":      "echo of request id",
  "type":    "topic name or method echo",
  "data":    {},
  "error":   "ERR_CODE if any",
  "message": "human-readable detail"
}
```

Every `SOR.*` message delivers `data` as an **array**. Payloads that are naturally a single object or scalar arrive as a one-element array; payloads that are naturally lists (such as order-book levels) are sent as-is, not wrapped again.

Prices and amounts are **decimal strings**; timestamps are epoch **milliseconds**. For a market `BASE-QUOTE`, "base" is the first currency and "quote" the second (e.g. for `BTC-EUR`, base = BTC, quote = USD).

## Topics

At a glance — subscribe to any of these via `{ "method": "subscribe", "events": [...] }`. `<pair>` is a market like `BTC-EUR`. Authenticated topics need a valid login (see above); private topics are delivered only to the owning account.

| Topic | Access | Snapshot on subscribe | Delivers |
|-------|--------|-----------------------|----------|
| [`SOR.PI.<pair>`](#sorpipair--price-index-public) | Public | No | Live price index aggregated across SOR venues. |
| [`SOR.OHLCV.<pair>.<timeframe>`](#sorohlcvpairtimeframe--ohlcv-candles-public) | Public | No | Live OHLCV candles (`1m`). |
| [`SOR.T.<pair>`](#sortpair--ticker-public-snapshot-on-subscribe-when-cached) | Public | Yes (if cached) | 24 h rolling ticker. |
| [`SOR.OB.<pair>`](#sorobpair--order-book-public) | Public | Each message is a full snapshot | Full order-book replacement. |
| [`SOR.EXECUTIONS[.<pair>]`](#sorexecutionspair--order-executions-authenticated) | **Auth** (owner only) | No | Updates to your own SOR orders as they settle; `<pair>` optional. |
| [`LEDGER`](#ledger--balance-updates-authenticated) | **Auth** (owner only) | No | Real-time balance updates. |

The server also exposes `SOR.PUB_TRADES.<pair>` (public trade fills, snapshot on subscribe) and `SOR.PRV_TRADES.<pair>` (your own fills, authenticated). These aren't detailed below yet.

---

#### `SOR.PI.<pair>` — price index *(public)*

Live **price index** for the pair — a single reference price aggregated across the SOR venues.

```json
{ "method": "subscribe", "events": ["SOR.PI.BTC-EUR"] }
```

Update — `data[0]` is the price, in quote currency:

```json
{ "type": "SOR.PI.BTC-EUR", "data": ["98750.00"] }
```

---

#### `SOR.OHLCV.<pair>.<timeframe>` — OHLCV candles *(public)*

Live candles for the pair. Currently supported timeframe: `1m`.

```json
{ "method": "subscribe", "events": ["SOR.OHLCV.BTC-EUR.1m"] }
```

Update:

```json
{
  "type": "SOR.OHLCV.BTC-EUR.1m",
  "data": [
    {
      "mkt":     "BTC-EUR",
      "o":       "98000.00",
      "h":       "99100.00",
      "l":       "97900.00",
      "c":       "98750.00",
      "t":       1716134400000,
      "tf":      "1m",
      "sor_qty": "12.54",
      "sor_amt": "1250000.00"
    }
  ]
}
```

| Field | Meaning |
|-------|---------|
| `mkt` | Market pair. |
| `o` / `h` / `l` / `c` | Open / high / low / close price (quote currency). |
| `t` | Candle open time, epoch ms. |
| `tf` | Timeframe (`1m`). |
| `sor_qty` | Volume traded in the candle, **base** currency. |
| `sor_amt` | Amount traded in the candle, **quote** currency. |

---

#### `SOR.T.<pair>` — ticker *(public, snapshot on subscribe when cached)*

24 h rolling ticker for the pair. On subscribe you receive the latest cached snapshot if one exists; if none is cached yet, the subscription succeeds without an initial message.

```json
{ "method": "subscribe", "events": ["SOR.T.BTC-EUR"] }
```

Update:

```json
{
  "type": "SOR.T.BTC-EUR",
  "data": [
    {
      "mkt": "BTC-EUR",
      "o":  "98000.00",
      "h":  "99100.00",
      "l":  "97900.00",
      "c":  "98750.00",
      "qty": "12.54",
      "amt": "1250000.00",
      "t":  1716134400000
    }
  ]
}
```

| Field | Meaning |
|-------|---------|
| `mkt` | Market pair. |
| `o` / `h` / `l` / `c` | Open / high / low / close price over the window (quote currency). |
| `qty` | Rolling volume, **base** currency. |
| `amt` | Rolling amount, **quote** currency. |
| `t` | Snapshot time, epoch ms. |

---

#### `SOR.OB.<pair>` — order book *(public)*

Full order-book snapshot for the pair. Each message is a **complete replacement** of the previous state — no incremental diffs.

```json
{ "method": "subscribe", "events": ["SOR.OB.BTC-EUR"] }
```

Update — `data` is a positional array `[ pair, bids, asks, timestamp ]`:

```json
{
  "type": "SOR.OB.BTC-EUR",
  "data": [
    "BTC-EUR",
    [
      ["98700.00", "1.5"],
      ["98650.00", "3.0"]
    ],
    [
      ["98750.00", "0.8"],
      ["98800.00", "2.1"]
    ],
    1716134401234
  ]
}
```

| Position | Meaning |
|----------|---------|
| `data[0]` | Market pair. |
| `data[1]` | Bids — array of `[price, size]` levels. |
| `data[2]` | Asks — array of `[price, size]` levels. |
| `data[3]` | Snapshot time, epoch ms. |

For each level, `price` is in quote currency and `size` is in base currency.

---

#### `SOR.EXECUTIONS[.<pair>]` — order executions *(authenticated)*

Real-time updates for **your own** SOR orders as they settle. Requires authentication and is delivered only to the connections of the account that owns the order — there is no snapshot on subscribe, you receive updates as they happen.

The market suffix is **optional**:

- `SOR.EXECUTIONS` — every order execution on your account, across all markets.
- `SOR.EXECUTIONS.<pair>` — only executions on that market.

The payload mirrors the trader REST `SorOrder` (same fields and the same integer enums for `side`/`type`/`tif`/`status`), so it lines up with the [place → poll flow](./place_order.md) — this topic is just the push counterpart to polling `GET /private/sor/orders/{client_order_id}`.

```json
{ "method": "subscribe", "events": ["SOR.EXECUTIONS.ETH-EUR"] }
```

Update — `data[0]` is the order:

```json
{
  "type": "SOR.EXECUTIONS.ETH-EUR",
  "data": [
    {
      "coid":        "019f4783-dd4f-776a-9a14-33640fe0a605",
      "mkt":         "ETH-EUR",
      "side":        1,
      "type":        1,
      "tif":         1,
      "qty":         "0.0328",
      "prc":         "1525",
      "amt":         "50.02",
      "fee":         "0.19",
      "matched_qty": "0.0328",
      "matched_amt": "49.7",
      "status":      3,
      "created_at":  1752075261274,
      "closed_at":   1752075262476,
      "updated_at":  1752075262476,
      "matches": [
        {
          "venue":          "kraken_prime",
          "venue_order_id": "33badac6-cfc4-4292-bcae-876858e49680",
          "venue_match_id": "57fb489d-d5fd-4d89-9987-e60ecf63e8d9",
          "qty":            "0.0328",
          "prc":            "1515.25",
          "amt":            "49.7",
          "fee":            "0",
          "fee_currency":   "EUR",
          "created_at":     1752075262476
        }
      ]
    }
  ]
}
```

| Field | Meaning |
|-------|---------|
| `coid` | Your `client_order_id` (the idempotency key you sent on placement). |
| `mkt` | Market pair. |
| `side` | `1` = buy, `2` = sell. |
| `type` | `1` = LIMIT. |
| `tif` | Time in force — `1` = FOK, `2` = IOC. |
| `qty` | Order quantity, **base** currency. |
| `prc` | Limit price, **quote** currency. |
| `amt` | Order amount, **quote** currency. |
| `fee` | Fee charged, **quote** currency. |
| `matched_qty` | Filled quantity so far, **base** currency. |
| `matched_amt` | Filled amount so far, **quote** currency. |
| `status` | `1` New, `2` PartiallyFilled, `3` Filled, `4` Cancelled, `5` Expired, `6` Rejected — see the [status table](./place_order.md#response-sororder). |
| `created_at` | Order creation time, epoch ms. |
| `closed_at` | Terminal (settlement) time, epoch ms; `null` while the order is still open. |
| `updated_at` | Time of this update, epoch ms. |
| `matches` | Individual fills; omitted when there are none. |

Each entry in `matches`:

| Field | Meaning |
|-------|---------|
| `venue` | Venue that filled the match. |
| `venue_order_id` | Order id at the venue. |
| `venue_match_id` | Match id at the venue. |
| `qty` | Matched quantity, **base** currency. |
| `prc` | Match price, **quote** currency. |
| `amt` | Matched amount, **quote** currency. |
| `fee` | Fee for the match. |
| `fee_currency` | Currency of `fee` (may be empty). |
| `created_at` | Match execution time, epoch ms. |

As with the REST flow, a terminal `status` is `3` Filled, `4` Cancelled, `5` Expired, or `6` Rejected — an unmatched FOK/IOC order settling as `4` Cancelled is expected, not an error.

---

#### `LEDGER` — balance updates *(authenticated)*

Real-time balance updates for your account. Requires authentication and is delivered only for the authenticated account; there is no snapshot on subscribe.

```json
{ "method": "subscribe", "events": ["LEDGER"] }
```

Update — `data` is a list of balance tuples `[ currency, vault_id, vault_type, balance ]`:

```json
{
  "type": "LEDGER",
  "data": [
    ["BTC", 0, "SPOT", "0.12345678"]
  ]
}
```

| Position | Meaning |
|----------|---------|
| `currency` | Currency code, e.g. `BTC`. |
| `vault_id` | Numeric identifier of the vault (integer). |
| `vault_type` | Vault classification, e.g. `SPOT`. |
| `balance` | Balance for that currency/vault (decimal string). |

## Example

A minimal client that mints a trader JWT, connects with the auth headers, subscribes to the
`BTC-EUR` spot price, and prints every message. Uses the [`websockets`](https://websockets.readthedocs.io/)
library — `uv run --with websockets --with pyjwt ws_example.py`.

```python
import asyncio, hashlib, json, os, time
import jwt        # pip install pyjwt
import websockets # pip install websockets

WS_URL = "wss://api.youngplatform.com/api/socket/ws"

def trader_jwt() -> str:
    # Connect/login carries no body, so hash_payload is sha256(b"").
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
            "events": ["SOR.PI.BTC-EUR"],
        }))
        async for raw in ws:
            print(json.loads(raw))

asyncio.run(main())
```

Public topics need no credentials — drop the `headers` argument and subscribe straight away.

## See also

- [API Key Authentication](./auth.md) — JWT claims, `hash_payload`, and ready-to-run token minters.
- [Placing an Order (SOR)](./place_order.md) — REST place → wait → poll flow for SOR orders.
- Repository [README](https://github.com/YoungAgency/api_examples/blob/v5/README.md).
