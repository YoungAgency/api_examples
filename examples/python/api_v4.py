import time
import hashlib
import jwt
import requests
import json



# Configuration variables
KEY_ID = ""  # Replace with your key ID string
PUBLIC_KEY = ""  # Replace with your public key string
PRIVATE_KEY = ""  # Replace with your private key string
BASE_URL = "https://api.youngplatform.com/api/v4/private"


def generate_jwt(public_key, private_key, payload=None):
    """
    Generate a JWT token with optional payload hashing.

    :param public_key: The public key string.
    :param private_key: The private key string.
    :param payload: The payload to include in the JWT hash (optional).
    :return: Encoded JWT token.
    """
    iat = int(time.time())
    exp = iat + 30

    # Use an empty string if no payload is provided
    payload = payload or ""

    # Hash the payload
    hash_payload = hashlib.sha256(payload.encode('utf-8')).hexdigest()

    # Define JWT claims
    jwt_claims = {
        "sub": public_key,
        "iat": iat,
        "exp": exp,
        "hash_payload": hash_payload,
    }

    # Generate and return the JWT token
    return jwt.api_jwt.encode(jwt_claims, private_key, algorithm="HS256")


def make_request(method, endpoint, jwt_token, payload=None):
    """
    Make an HTTP request to the API.

    :param method: HTTP method (GET or POST).
    :param endpoint: API endpoint to call.
    :param jwt_token: JWT token for authentication.
    :param payload: JSON payload for POST requests (optional).
    :return: Response object.
    """
    headers = {
        "Authorization": jwt_token,
        "X-Api-Key-Id": KEY_ID,
    }
    if payload:
        headers["Content-Type"] = "application/json"

    url = f"{BASE_URL}/{endpoint}"

    # Send the appropriate request
    if method == "GET":
        response = requests.get(url, headers=headers)
    elif method == "POST":
        response = requests.post(url, headers=headers, data=json.dumps(payload))
    else:
        raise ValueError("Unsupported HTTP method")

    # Handle errors
    if response.status_code != 200:
        print(f"Error: {response.status_code}\n{response.text}")
        exit()

    return response


def main():
    # Generate a JWT token for a GET request
    jwt_token = generate_jwt(PUBLIC_KEY, PRIVATE_KEY)

    # GET request for balances
    balances_response = make_request("GET", "balances", jwt_token)
    print(balances_response.json())

    # Payload for cancelling an order
    cancel_order_payload = {
        "orderId": 100
    }

    # Generate a JWT token for a POST request
    jwt_token_body = generate_jwt(PUBLIC_KEY, PRIVATE_KEY, json.dumps(cancel_order_payload))

    # POST request to cancel an order
    cancel_response = make_request("POST", "cancel", jwt_token_body, cancel_order_payload)
    print(cancel_response.json())


if __name__ == "__main__":
    main()
