import time
import hashlib
import jwt
import requests
import json

key_id = None # Replace with your key ID string
public_key = None # Replace with your public key string
private_key = None # Replace with your private key string

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



# generate a JWT token for GET request
jwtToken = generate_jwt(public_key, private_key)
headers = {
    "Authorization": jwtToken,
    "X-Api-Key-Id": key_id
}

req_url = "https://api.youngplatform.com/api/v4/private/balances"
response = requests.get(req_url, headers=headers)

if response.status_code != 200:
    print(f"Error: {response.status_code}")
    print(response.text)
    exit()
body = response.json()

print(body)

# jwt for POST request

# payload for cancel order
cancel_order_payload = {
    "orderId": 100
}

# generate a JWT token for POST request
body_string = json.dumps(cancel_order_payload)
jwtTokenBody = generate_jwt(public_key, private_key, body_string)

headers = {
    "Authorization": jwtTokenBody,
    "X-Api-Key-Id": key_id,
    "Content-Type": "application/json"
}
req_url = "https://api.youngplatform.com/api/v4/private/cancel"
response = requests.post(req_url, headers=headers, data=body_string)

if response.status_code != 200:
    print(f"Error: {response.status_code}")
    print(response.text)
    exit()