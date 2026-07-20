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
            "events": ["SOR.PI.BTC-EUR", "SOR.EXECUTIONS"],
        }))
        async for raw in ws:
            print(json.loads(raw))

asyncio.run(main())