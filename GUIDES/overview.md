# Overview

The **Young Platform Trader API** gives programmatic access to real-time market data and **Smart Order Routing (SOR)** trading.

The same account and API keys work across two interfaces — _REST and WebSocket_ — so you can poll or stream.

## Base URL

The REST trader surface is versioned under `/api/v1/trader`:

| Environment | Base URL |
|-------------|----------|
| Production | `https://api.youngplatform.com/api/v1/trader` |

The WebSocket API is served at `/api/socket/ws` on the same host.

## Surfaces

The API is split by access level. The REST trader surface has two paths under `/api/v1/trader`:

| Surface | Purpose | Auth |
|---------|---------|------|
| `/api/v1/trader/public/…` | Market data — markets, ticker, liquidity, charts. | **None.** |
| `/api/v1/trader/private/…` | Account actions — balance, profile, place & read SOR orders. | **API-key auth.** |

## Interfaces

- **REST** — request/response over HTTP. The full contract is in the [OpenAPI reference](../docs/openapi.html). Start with [Placing an Order (SOR)](./place_order.md).
- **WebSocket** — subscribe to live prices, candles, order book, and account balances over a single connection. See [WebSocket API](./websocket.md).

## Authentication

Public market data needs no credentials.

Everything else is authenticated with:
1. an `X-Api-Key-Id` header, plus an `aud: "trader"` claim in the JWT. Generate API keys at pro.youngplatform.com.
2. a short-lived **HS256 JWT** (signed with your API key) 

See [API Key Authentication](./auth.md) for the full claim reference and ready-to-run token minters.

## Conventions

- **Markets** are strings in `BASE-QUOTE` form, e.g. `BTC-EUR` — base currency first, quote second.
- **Prices and amounts** are exact **decimal strings** (never floats), to avoid rounding error.
- **Timestamps** are ISO-8601 UTC on REST; the WebSocket API uses epoch **milliseconds**.

## Next steps

- [API Key Authentication](./auth.md) — mint a token and make your first authenticated call.
- [Placing an Order (SOR)](./place_order.md) — the place → poll flow for SOR orders.
- [WebSocket API](./websocket.md) — live market data and balance streams.
- [OpenAPI reference](../docs/openapi.html) — full request/response schemas.
