import websocket
import json
import time
import hashlib
import jwt # PyJWT library


wss_url = 'wss://api.youngplatform.com/api/socket/ws'

key_id = None # Replace with your key ID string
public_key = None # Replace with your public key string
private_key = None # Replace with your private key string

# Define the subscription payload
subscribe_payload = {
    "method": "subscribe",
    "events": [
        "T.BTC-EUR",  # ticker
        "TH.BTC-EUR",  # trade history
        "OBI.BTC-EUR",  # order book
    ]
}

def on_open(ws):
    print("Connected to the WSS server.")
    ws.send(json.dumps(subscribe_payload))

def on_message(ws, message):
    print("Message received:")
    print(message)

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("Connection closed.")

def generate_jwt(public_key, private_key, payload=None):
    # Get the current timestamp and set expiration (30 seconds from now)
    iat = int(time.time())
    exp = iat + 30

    # If payload is None, use an empty string
    if payload is None:
        payload = ""

    # Generate a SHA-256 hash of the payload
    hash_payload = hashlib.sha256(payload.encode('utf-8')).hexdigest()

    # Define the JWT claims
    jwt_claims = {
        "sub": public_key,
        "iat": iat,
        "exp": exp,
        "hash_payload": hash_payload
    }

    # Generate the JWT token
    token = jwt.api_jwt.encode(jwt_claims, private_key, algorithm="HS256")

    return token



jwtToken = None
if public_key and private_key:
    # Generate a JWT token
    jwtToken = generate_jwt(public_key, private_key, "")

# Define the headers for the WebSocket request
headers = {
    "Authorization": jwtToken,  # Replace with your access token if required
    "X-Api-Key-Id": key_id
}

# Create a WebSocket connection with headers
ws = websocket.WebSocketApp(
    wss_url,
    on_open=on_open,
    on_message=on_message,
    on_error=on_error,
    on_close=on_close
)
if jwtToken:
    # add the headers to the websocket to use private channels
    ws.header = headers

# Run the WebSocket client
ws.run_forever()


