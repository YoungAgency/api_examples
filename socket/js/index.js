const WebSocket = require('ws');
const crypto = require('crypto');

const wssURL = 'wss://api.youngplatform.com/ws';

const ws = new WebSocket(wssURL);

const apiSecret = process.env.YOUNG_API_SECRET;
if (!apiSecret) {
    console.error('Missing YOUNG_API_SECRET environment variable.');
    process.exit(1);
}

const apiKey = process.env.YOUNG_API_KEY;
if (!apiKey) {
    console.error('Missing YOUNG_API_KEY environment variable.');
    process.exit(1);
}

ws.on('open', () => {
    console.log('Connected to the WSS server.');

    // Login to socket

    // Create an HMAC-SHA512 hash
    const hmac = crypto.createHmac('sha512', apiSecret);

    var nowUnix = Math.floor(Date.now() / 1000);
    var authMessage = 'YAUTH' + nowUnix;
    hmac.update(authMessage);

    // Calculate the hash in hexadecimal format
    const hmacHex = hmac.digest('hex');

    var authPayload = {
        op: 'AUTH',
        data: {
            apiKey: apiKey,
            timestamp: nowUnix,
            signature: hmacHex
        }
    }
    ws.send(JSON.stringify(authPayload));
});

ws.on('message', (message) => {
    // console.log(`Received message from server: ${message}`);
    console.log(message.toString());
    var parsedMessage = JSON.parse(message);
    if (parsedMessage.data === 'logged') {
        // subscribe to balance
        var subscribePayload = {
            op: 'SUBSCRIBE',
            channel: 'BAL'
        }
        ws.send(JSON.stringify(subscribePayload));

        // subscribe to order update for BTC-EUR
        subscribePayload = {
            op: 'SUBSCRIBE',
            channel: 'OU',
            data: {
                pairs: ['BTC-EUR']
            }
        }
        ws.send(JSON.stringify(subscribePayload));

        // subscribe to order book update for BTC-EUR
        subscribePayload = {
            op: 'SUBSCRIBE',
            channel: 'OB',
            data: {
                pairs: ['BTC-EUR']
            }
        }
        ws.send(JSON.stringify(subscribePayload));
    } else {
        switch (parsedMessage.channel) {
            case 'BAL':
                console.log('Balance update: ', parsedMessage.data);
                break;
            case 'OU':
                console.log('Order update: ', parsedMessage.data);
                break;
            case 'OB':
                console.log('Order book update: ', parsedMessage.data);
                break;
            default:
                console.log('Unknown channel: ', parsedMessage.channel, message.toString());
        }
    }
});

ws.on('close', (code, reason) => {
    console.log('Disconnected from the WSS server.', code, reason.toJSON());
});

ws.on('error', (error) => {
    console.error(`WebSocket error: ${error.message}`);
});
