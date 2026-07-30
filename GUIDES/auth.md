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

## Optional: ES256 (ECDSA) keys

Everything above uses **HS256**, where the same secret signs and verifies. If you'd rather
the server never hold a key that can *mint* your tokens, you can enrol your own **ECDSA
secp256r1 (P-256)** key pair and sign with **ES256** instead. Claims, headers, lifetime and
`hash_payload` are unchanged — only the key and the `alg` differ.

### Generating the key pair

Generate the pair, then convert both halves to base64-encoded DER:

```bash
# generate ecdsa keys
openssl ecparam -name secp256r1 -genkey -noout -out private_key_ecdsa.pem
openssl ec -in private_key_ecdsa.pem -pubout -out public_key_ecdsa.pem

# generate der format
openssl ec -in private_key_ecdsa.pem -outform DER | base64 > private_key_ecdsa.der
openssl ec -in public_key_ecdsa.pem -pubin -outform DER | base64 > public_key_ecdsa.der
```

- **`public_key_ecdsa.der`** — paste its contents into the public-key field of the API-key
  form at pro.youngplatform.com when you create the key. This is what the server verifies
  your tokens against.
- **`private_key_ecdsa.der`** — keep it secret; its contents go in `YP_PRIVATE_KEY` and sign
  each token. It never leaves your machine.

### Signing

Base64-decode `YP_PRIVATE_KEY` back to DER, load it as an EC private key, and sign with
`ES256`. This needs `cryptography` alongside PyJWT (`pip install "pyjwt[crypto]"`):

```python
import base64, hashlib, os, time
import jwt  # pip install "pyjwt[crypto]"
from cryptography.hazmat.primitives.serialization import load_der_private_key

# contents of private_key_ecdsa.der; `base64` wraps lines, so strip whitespace
der = base64.b64decode("".join(os.environ["YP_PRIVATE_KEY"].split()))
signing_key = load_der_private_key(der, password=None)

iat = int(time.time())
token = jwt.encode(
    {
        "sub": os.environ["YP_PUBLIC_KEY"],
        "aud": "trader",
        "iat": iat,
        "exp": iat + 30,
        "hash_payload": hashlib.sha256(b"").hexdigest(),
    },
    signing_key,
    algorithm="ES256",
)
```

The ready-made minter does this for you when `YP_JWT_ALG=ES256`:

```bash
export YP_JWT_ALG=ES256
export YP_PRIVATE_KEY="$(cat private_key_ecdsa.der)"   # instead of the HS256 secret
uv run examples/python/trader_jwt/trader_jwt.py
```

`YP_JWT_ALG` defaults to `HS256`, so leaving it unset keeps the behaviour described earlier
in this guide.

## See also

- [ES256 (ECDSA) keys](#optional-es256-ecdsa-keys) — bring your own key pair instead of a shared secret.
- [Placing an Order (SOR)](./place_order.md) — full POST request/response schema, place → wait → poll example.
- REST and WebSocket usage in the repository [README](https://github.com/YoungAgency/youngplatform_api_docs/blob/main/README.md).
