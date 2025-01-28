const WebSocket = require('ws');
const jwt = require('jsonwebtoken');
const crypto = require('crypto');

// Configuration variables
const WSS_URL = 'wss://api.youngplatform.com/api/socket/ws';
const KEY_ID = ""; // Your key ID
const PUBLIC_KEY = ""; // Your public key
const PRIVATE_KEY = ""; // Your private key

/**
 * Generate a JWT token with optional payload hashing.
 * @param {string} publicKey - The public key string.
 * @param {string} privateKey - The private key string.
 * @param {string} [payload] - The payload to include in the JWT hash (optional).
 * @returns {string} - Encoded JWT token.
 */
function generateJwt(publicKey, privateKey, payload = "") {
    const iat = Math.floor(Date.now() / 1000);
    const exp = iat + 30;
    
    // Hash the payload
    const hashPayload = crypto.createHash('sha256').update(payload).digest('hex');

    // Define JWT claims
    const jwtClaims = {
        "sub": publicKey,
        "iat": iat,
        "exp": exp,
        "hash_payload": hashPayload
    };

    // Generate and return the JWT token
    return jwt.sign(jwtClaims, privateKey, { algorithm: 'HS256' });
}

// Generate the JWT token for authentication
const token = generateJwt(PUBLIC_KEY, PRIVATE_KEY);

// WebSocket connection options
const headers = {
    "Authorization": token,
    "X-Api-Key-Id": KEY_ID,
};
const ws = new WebSocket(WSS_URL, { headers });

// Event handlers
ws.on('open', () => {
    console.log('Connected to the WSS server.');

    const subscribePayload = {
        method: 'subscribe',
        events: [
            "T.BTC-EUR",    // # ticker,
            "TH.BTC-EUR",   // # trade history public
            "OBI.BTC-EUR",  // # order book incremental
            "TP.BTC-EUR",   // # trade history private
            "PO.BTC-EUR",   // # private orders
            "BL",           // # balances
        ]
    };

    ws.send(JSON.stringify(subscribePayload));
});

ws.on('message', (message) => {
    console.log(message.toString());
});
