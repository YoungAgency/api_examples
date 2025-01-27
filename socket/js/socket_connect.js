const WebSocket = require('ws');
const jwt = require('jsonwebtoken');
const crypto = require('crypto');

const wssURL = 'wss://api.youngplatform.com/api/socket/ws';

const keyId = ""; // your key id
const publicKey = ""; // your public key
const privateKey = ""; // your private key
const token = generateJwt(publicKey,privateKey, "");

const headers = {
    "Authorization": token,
    "X-Api-Key-Id": keyId,
}
const ws = new WebSocket(wssURL, options = { headers: headers });

ws.on('open', async () => {
    console.log('Connected to the WSS server.');

    let subscribePayload = {
        method: 'subscribe',
        events: [
            'T.BTC-EUR', // ticker
            "TP.BTC-EUR", // trade history
            "PO.BTC-EUR", // order book snapshot
        ]
    }
    ws.send(JSON.stringify(subscribePayload));
});

ws.on('message', async (message) => {
    console.log(message.toString())
});



function generateJwt(publicKey, privateKey, payload) {
    let iat = Math.floor(Date.now() / 1000);
    let exp = iat + 30;
    if (payload == undefined) {
        // if GET request or no payload, use empty string
        payload = "";
    }
    let hashPayload = crypto.createHash('sha256').update(payload).digest('hex');
    const jwtClaims = {
        "sub": publicKey,
        "iat": iat,
        "exp": exp,
        "hash_payload": hashPayload
    };
    let token = jwt.sign(jwtClaims, privateKey, { algorithm: 'HS256' });
   return token;
}