# Young Platform API Examples

Examples and guides for connecting to the **Young Platform API** — real-time market
data and Smart Order Routing (SOR) trading, exposed over REST and WebSocket.

The trader surface is versioned under `/api/v1/trader`:

- `/api/v1/trader/public/…` — market data (markets, ticker, liquidity, charts). **No authentication.**
- `/api/v1/trader/private/…` — account-scoped requests (balance, profile, place/read SOR orders). **API-key auth.**

The full contract is in [trader_openapi.json](./trader_openapi.json) (OpenAPI 3.0),
rendered as browsable reference docs at
**[youngagency.github.io/youngplatform_api_docs](https://youngagency.github.io/youngplatform_api_docs/)**.

## Authentication

Every authenticated request carries a short-lived **HS256 JWT** (signed with your
API key) plus an `X-Api-Key-Id` header. Generate API keys at pro.youngplatform.com.
See the guide for the full reference.

- **[GUIDES/jwt.md](./GUIDES/jwt.md)** — JWT claims, `hash_payload`, and ready-to-run token minters.

## Examples

All examples are Python and run with [uv](https://docs.astral.sh/uv/).

| Path | What it does |
|------|--------------|
| [examples/python/trader_jwt/](./examples/python/trader_jwt/trader_jwt.py) | Standalone minter for a body-bound **trader** JWT — prints the `Authorization` / `X-Api-Key-Id` headers. |
| [examples/python/trader_sdk/](./examples/python/trader_sdk/) | Full example: a generated SDK (from the OpenAPI spec) + a tester that exercises every trader endpoint. See its [README](./examples/python/trader_sdk/README.md). |

The token minter is a self-contained script with inline dependencies — run it
directly, no setup:

```bash
uv run examples/python/trader_jwt/trader_jwt.py
```

## License

See [LICENSE](./LICENSE).
