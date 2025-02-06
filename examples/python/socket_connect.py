import websocket
import json
import time
import hashlib
import jwt  # PyJWT library

# Configuration variables
WSS_URL = 'wss://api.youngplatform.com/api/socket/ws'
KEY_ID = None  # Replace with your key ID string
PUBLIC_KEY = None # Replace with your public key string
PRIVATE_KEY = None  # Replace with your private key string

# Define the subscription payload
SUBSCRIBE_PAYLOAD = {
    "method": "subscribe",
    "events": [
        "T.BTC-EUR",    # ticker,
        "TH.BTC-EUR",   # trade history public
        "OBI.BTC-EUR",  # order book incremental
        "TP.BTC-EUR",   # trade history private
        "PO.BTC-EUR",   # private orders
        "BL",           # balances
    ]
}

def on_open(ws):
    """Callback executed when the WebSocket connection is opened."""
    print("Connected to the WSS server.")
    ws.send(json.dumps(SUBSCRIBE_PAYLOAD))

def on_message(ws, message):
    """Callback executed when a message is received."""
    print("Message received:")
    print(message)

def on_error(ws, error):
    """Callback executed when an error occurs."""
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    """Callback executed when the WebSocket connection is closed."""
    print("Connection closed.")

def generate_jwt(public_key, private_key, payload=None):
    """Generate a JWT token with optional payload hashing.

    Args:
        public_key (str): The public key string.
        private_key (str): The private key string.
        payload (str, optional): The payload to include in the JWT hash.

    Returns:
        str: Encoded JWT token.
    """
    iat = int(time.time())
    exp = iat + 30

    # If payload is None, use an empty string
    payload = payload or ""

    # Generate a SHA-256 hash of the payload
    hash_payload = hashlib.sha256(payload.encode('utf-8')).hexdigest()

    # Define the JWT claims
    jwt_claims = {
        "sub": public_key,
        "iat": iat,
        "exp": exp,
        "hash_payload": hash_payload
    }

    # Generate and return the JWT token
    return jwt.api_jwt.encode(jwt_claims, private_key, algorithm="HS256")

# Generate a JWT token if keys are provided
jwt_token = generate_jwt(PUBLIC_KEY, PRIVATE_KEY, "") if PUBLIC_KEY and PRIVATE_KEY else None

# Define the headers for the WebSocket request
HEADERS = {
    "Authorization": jwt_token,
    "X-Api-Key-Id": KEY_ID
} if jwt_token else {}

# Create a WebSocket connection with headers
ws = websocket.WebSocketApp(
    WSS_URL,
    on_open=on_open,
    on_message=on_message,
    on_error=on_error,
    on_close=on_close
)

# Add headers to the WebSocket connection if JWT token is available
if jwt_token:
    ws.header = HEADERS

# Run the WebSocket client
ws.run_forever()
