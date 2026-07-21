"""Per-request trader authentication for httpx.

The Youngplatform trader API authenticates every request with a short-lived
HS256 JWT signed by your API key, plus an ``X-Api-Key-Id`` header. The token is
body-bound: it carries a ``hash_payload`` claim equal to ``sha256(request body)``
and lives at most 60 seconds, so it is effectively single-use and cannot be
replayed against a different body.

``TraderAuth`` implements ``httpx.Auth`` so a fresh, correctly-bound token is
minted for *every* outgoing request — including the empty-body GETs the trader
API exposes today (``hash_payload`` is then ``sha256("")``). Pass an instance to
the generated client via ``httpx_args={"auth": TraderAuth(...)}``.

See GUIDES/jwt.md for the full claim reference.
"""

from __future__ import annotations

import hashlib
import time
from collections.abc import Generator

import httpx
import jwt  # PyJWT

# aud claim binding the token to the trader HTTP surface.
TRADER_AUDIENCE = "trader"
# Server caps the trader token lifetime at 60s; stay just under it.
TOKEN_TTL_SECONDS = 30


class TraderAuth(httpx.Auth):
    """Signs each request with a fresh, body-bound trader JWT.

    key_id      -> sent as the X-Api-Key-Id header
    public_key  -> JWT ``sub`` claim (your enrolled public identifier)
    private_key -> HS256 signing secret
    """

    # httpx needs the request body available before auth_flow runs so we can hash it.
    requires_request_body = True

    def __init__(self, key_id: str, public_key: str, private_key: str) -> None:
        self._key_id = key_id
        self._public_key = public_key
        self._private_key = private_key

    def auth_flow(
        self, request: httpx.Request
    ) -> Generator[httpx.Request, httpx.Response, None]:
        token = self._mint(request.content or b"")
        request.headers["Authorization"] = f"Bearer {token}"
        request.headers["X-Api-Key-Id"] = self._key_id
        yield request

    def _mint(self, body: bytes) -> str:
        now = int(time.time())
        claims = {
            "sub": self._public_key,
            "aud": TRADER_AUDIENCE,
            "iat": now,
            "exp": now + TOKEN_TTL_SECONDS,
            "hash_payload": hashlib.sha256(body).hexdigest(),
        }
        return jwt.encode(claims, self._private_key, algorithm="HS256")
