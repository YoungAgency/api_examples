# /// script
# requires-python = ">=3.11"
# dependencies = ["pyjwt>=2.8"]
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
    export YP_PRIVATE_KEY=...   # HS256 signing secret

Run with:

    uv run trader_token.py                 # empty body (GET / WebSocket login)
    uv run trader_token.py --body '{"market":"BTC-EUR"}'   # hash a JSON body

Paste the printed headers into your HTTP/WebSocket client (see GUIDES/jwt.md).
"""

import argparse
import hashlib
import os
import time

import jwt  # PyJWT

TRADER_AUDIENCE = "trader"
# Server caps the trader token lifetime at 60s; stay just under it.
TOKEN_TTL = 30  # seconds


def generate_trader_jwt(
    public_key: str, private_key: str, body: bytes = b"", ttl: int = TOKEN_TTL
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
    return jwt.encode(claims, private_key, algorithm="HS256")


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

    token = generate_trader_jwt(public_key, private_key, args.body.encode())

    # Paste these into your HTTP/WebSocket client (see GUIDES/jwt.md).
    print(f"X-Api-Key-Id: {key_id}")
    print(f"Authorization: Bearer {token}")
