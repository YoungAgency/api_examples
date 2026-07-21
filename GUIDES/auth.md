# API Key Authentication

> ⚠️ **Migrating from the v4 APIs?** JWTs must now carry an `aud` claim of `"trader"`, identifying the surface — this is a **required change**. See Python snippets below.

Every authenticated Young Platform request carries a short-lived **JWT** signed with your API key. The same credentials work across both surfaces — REST and WebSocket.

## Credentials

Generate API keys at pro.youngplatform.com. You get three values:

- **KEY_ID** — identifies the key; sent in the `X-Api-Key-Id` header.
- **PUBLIC_KEY** — the enrolled public identifier; goes in the JWT `sub` claim.
- **PRIVATE_KEY** — the HS256 signing secret.

Every request carries two headers:

- **`Authorization`**: `Bearer <JWT>`
- **`X-Api-Key-Id`**: your `KEY_ID`

## Claims

All tokens are signed **HS256** with your `PRIVATE_KEY`. The claim set is:

| Claim | REST / WebSocket |
|-------|------------------|
| `sub` | `PUBLIC_KEY` |
| `aud` | `"trader"` |
| `iat` | now (epoch seconds) |
| `exp` | ≤ `iat` + 60s |
| `hash_payload` | SHA-256 hex of the request body |

- **`aud` is required** and must be `"trader"`.
- **REST/WebSocket tokens are short-lived and body-bound.** The 60s lifetime plus `hash_payload` makes each token effectively single-use and non-replayable against a different body. Mint a fresh token per request.

### hash_payload

For REST/WebSocket, `hash_payload` is the SHA-256 hex digest of the request body:

- **Empty string (`""`)** for **GET requests** and **WebSocket login** (no body).
- **`sha256(body)`** for requests that carry a JSON body (e.g. a POST).

## Example scripts

Set your credentials first — every snippet below reads them from the environment:

```bash
export YP_KEY_ID=...        # X-Api-Key-Id header
export YP_PUBLIC_KEY=...    # JWT "sub"
export YP_PRIVATE_KEY=...   # HS256 signing secret
```

The Python examples use [PyJWT](https://pyjwt.readthedocs.io/). Each linked script is standalone with inline dependencies — run it with `uv run` and it installs PyJWT on its own, no setup required.

### Trader

Mint a fresh, body-bound token per request:

```python
import hashlib, os, time
import jwt  # pip install pyjwt

def trader_jwt(body: bytes = b"") -> str:
    iat = int(time.time())
    claims = {
        "sub": os.environ["YP_PUBLIC_KEY"],
        "aud": "trader",       # NEW
        "iat": iat,
        "exp": iat + 30,       # ≤ 60s server cap
        "hash_payload": hashlib.sha256(body).hexdigest(),
    }
    return jwt.encode(claims, os.environ["YP_PRIVATE_KEY"], algorithm="HS256")

token = trader_jwt(b'{"market":"BTC-EUR"}')  # b"" for GET / WebSocket login
print(f"Authorization: Bearer {token}")
print(f"X-Api-Key-Id: {os.environ['YP_KEY_ID']}")
```

Or run the ready-made minter:

```bash
uv run examples/python/trader_jwt/trader_jwt.py                              # empty body (GET / WebSocket login)
uv run examples/python/trader_jwt/trader_jwt.py --body '{"market":"BTC-EUR"}' # bind to a JSON body
```

See [trader_jwt.py](https://github.com/YoungAgency/youngplatform_api_docs/blob/main/examples/python/trader_jwt/trader_jwt.py). Because the token is body-bound and short-lived, mint it **per request**; the generated SDK does this automatically via `young_auth.TraderAuth` (an `httpx.Auth` that hashes each request body and sets both headers) — see [trader_sdk/](https://github.com/YoungAgency/youngplatform_api_docs/tree/main/examples/python/trader_sdk).

#### Bare GET example (no SDK)

Minting the token and calling a GET endpoint directly with `requests`, no generated SDK involved. GET has no body, so `hash_payload` is the hash of the empty string:

```python
import hashlib, os, time
import jwt       # pip install pyjwt
import requests  # pip install requests

iat = int(time.time())
token = jwt.encode(
    {
        "sub": os.environ["YP_PUBLIC_KEY"],
        "aud": "trader",
        "iat": iat,
        "exp": iat + 30,
        "hash_payload": hashlib.sha256(b"").hexdigest(),  # empty body -> hash of b""
    },
    os.environ["YP_PRIVATE_KEY"],
    algorithm="HS256",
)

resp = requests.get(
    "https://api.youngplatform.com/api/v1/trader/private/balance",
    headers={
        "Authorization": f"Bearer {token}",
        "X-Api-Key-Id": os.environ["YP_KEY_ID"],
    },
)
print(resp.status_code, resp.json())
```

The `hash_payload` claim must be the SHA-256 hex digest of the **exact bytes** sent as the body — for a GET (no body) that's `sha256(b"")`; for a POST, hash after serializing and send that same serialization.

**Placing an order (POST)** — see the [Placing an Order guide](./place_order.md) for the full request/response schema and a place → wait → poll example.

## See also

- [Placing an Order (SOR)](./place_order.md) — full POST request/response schema, place → wait → poll example.
- REST and WebSocket usage in the repository [README](https://github.com/YoungAgency/youngplatform_api_docs/blob/main/README.md).
