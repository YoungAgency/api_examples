# /// script
# requires-python = ">=3.11"
# dependencies = ["pyjwt[crypto]>=2.8"]
# ///
"""Mint a short-lived, body-bound trader API token.

The trader HTTP/WebSocket surface uses a compact claim set: the
audience is "trader", the token lives at most 60 seconds, and it carries a
``hash_payload`` claim equal to ``sha256(request body)``. That makes each token
effectively single-use and non-replayable against a different body, so you mint
a fresh one per request.

Reads credentials from the environment (same names as the other examples):

    export YP_KEY_ID=...        # X-Api-Key-Id header
    export YP_PUBLIC_KEY=...    # JWT "sub"
    export YP_PRIVATE_KEY=...   # signing key (see YP_JWT_ALG)
    export YP_JWT_ALG=HS256     # optional, defaults to HS256

``YP_JWT_ALG`` selects how ``YP_PRIVATE_KEY`` is interpreted:

- ``HS256`` (default) — the key is the shared signing secret, used verbatim.
- ``ES256`` — the key is the base64 of a DER-encoded EC private key (secp256r1),
  i.e. the contents of::

      openssl ec -in private_key_ecdsa.pem -outform DER | base64

  The matching ``openssl ec -pubout -outform DER | base64`` is what you paste
  into the API-key form at pro.youngplatform.com. See GUIDES/auth.md.

Run with:

    uv run trader_token.py                 # empty body (GET / WebSocket login)
    uv run trader_token.py --body '{"market":"BTC-EUR"}'   # hash a JSON body
    YP_JWT_ALG=ES256 uv run trader_token.py               # sign with an EC key

Paste the printed headers into your HTTP/WebSocket client (see GUIDES/jwt.md).
"""

import argparse
import base64
import binascii
import hashlib
import os
import time

import jwt  # PyJWT

TRADER_AUDIENCE = "trader"
# Server caps the trader token lifetime at 60s; stay just under it.
TOKEN_TTL = 30  # seconds
DEFAULT_ALG = "HS256"
SUPPORTED_ALGS = ("HS256", "ES256")


def load_signing_key(private_key: str, alg: str):
    """Turn YP_PRIVATE_KEY into something jwt.encode can sign with under ``alg``."""
    if alg == "HS256":
        return private_key  # symmetric: the secret is used as-is
    if alg == "ES256":
        # cryptography ships with pyjwt[crypto]; only the EC path needs it.
        from cryptography.hazmat.primitives.serialization import load_der_private_key

        try:
            # `openssl ... | base64` wraps its output, so drop any whitespace first.
            der = base64.b64decode("".join(private_key.split()), validate=True)
            return load_der_private_key(der, password=None)
        except (binascii.Error, ValueError) as exc:
            raise SystemExit(
                "YP_PRIVATE_KEY must be the base64 of a DER-encoded EC private key "
                f"when YP_JWT_ALG=ES256 ({exc})"
            ) from exc
    raise SystemExit(f"Unsupported YP_JWT_ALG {alg!r}: expected one of {', '.join(SUPPORTED_ALGS)}")


def generate_trader_jwt(
    public_key: str,
    private_key: str,
    body: bytes = b"",
    ttl: int = TOKEN_TTL,
    alg: str = DEFAULT_ALG,
) -> str:
    iat = int(time.time())
    claims = {
        "sub": public_key,      # your public key
        "aud": TRADER_AUDIENCE,  # binds the token to the trader surface
        "iat": iat,
        "exp": iat + ttl,        # ≤ 60s server cap
        # sha256 of the request body; sha256(b"") for GET / WebSocket login.
        "hash_payload": hashlib.sha256(body).hexdigest(),
    }
    return jwt.encode(claims, load_signing_key(private_key, alg), algorithm=alg)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--body",
        default="",
        help="request body to bind the token to (default: empty, for GET / WS login)",
    )
    args = parser.parse_args()

    key_id = os.environ.get("YP_KEY_ID")
    public_key = os.environ.get("YP_PUBLIC_KEY")
    private_key = os.environ.get("YP_PRIVATE_KEY")
    alg = os.environ.get("YP_JWT_ALG", DEFAULT_ALG).upper()

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

    token = generate_trader_jwt(public_key, private_key, args.body.encode(), alg=alg)

    # Paste these into your HTTP/WebSocket client (see GUIDES/jwt.md).
    print(f"X-Api-Key-Id: {key_id}")
    print(f"Authorization: Bearer {token}")
