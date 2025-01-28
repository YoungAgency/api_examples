const axios = require('axios');
const crypto = require('crypto');
const jwt = require('jsonwebtoken');

// Configuration variables
const API_URL = 'https://api.youngplatform.dev';
const KEY_ID ="137aeb9bbebb4b9c8ce23a74c828e4d2"  // # Replace with your key ID string
const PUBLIC_KEY ="WUMD+WtGFzjDIDlQei0k5VVvZI4Bdfubutuz8wY5sfY="  // # Replace with your public key string
const PRIVATE_KEY ="IBQH9LbPQ7fqP45eKCop2M3UlKYvlNrU3F/zcHpR5wN7w5J+1A77eGUChw8932bS"  // # Replace with your private key string

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

/**
 * Fetch user balances.
 * @returns {Promise<Object>} - Balance data.
 */
async function getBalance() {
    try {
        const url = `${API_URL}/api/v4/private/balances`;
        const token = generateJwt(PUBLIC_KEY, PRIVATE_KEY);
        const headers = {
            "Authorization": token,
            "X-Api-Key-Id": KEY_ID,
        };
        const response = await axios.get(url, { headers });
        return response.data;
    } catch (error) {
        console.error("Error fetching balances:", error);
        throw error;
    }
}

/**
 * Cancel an order by ID.
 * @param {string} orderId - The ID of the order to cancel.
 * @returns {Promise<Object>} - Response data from the API.
 */
async function cancelOrder(orderId) {
    try {
        const url = `${API_URL}/api/v4/private/cancel`;
        const body = { orderId };
        const bodyString = JSON.stringify(body);
        const token = generateJwt(PUBLIC_KEY, PRIVATE_KEY, bodyString);
        const headers = {
            "Authorization": token,
            "X-Api-Key-Id": KEY_ID,
            "Content-Type": "application/json",
        };
        const response = await axios.post(url, bodyString, { headers });
        return response.data;
    } catch (error) {
        if (error.response && error.response.status === 400) {
            return error.response.data;
        }
        console.error("Error cancelling order:", error);
        throw error;
    }
}

// Main execution flow
(async () => {
    try {
        const balanceData = await getBalance();
        console.log("Balances:", balanceData);

        const cancelResponse = await cancelOrder("1");
        console.log("Cancel Order Response:", cancelResponse);
    } catch (error) {
        console.error("Error in main flow:", error);
    }
})();
