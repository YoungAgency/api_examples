const WebSocket = require('ws');
const axios = require('axios');
const jwt = require('jsonwebtoken');
const crypto = require('crypto');

const wssURL = 'wss://api.youngplatform.com/api/socket/ws';
const apiUrl = 'https://api.youngplatform.com';

const ws = new WebSocket(wssURL);

var localBookSnapshot = undefined;

console.log("Generating JWT token");

console.log(generateJwt("YOUR_API_KEY", "YOUR_PRIVATE"));


ws.on('open', async () => {
    console.log('Connected to the WSS server.');

    let subscribePayload = {
        op: 'SUBSCRIBE',
        channel: 'OBI',
        data: {
            pairs: ['BTC-EUR']
        }
    }
    ws.send(JSON.stringify(subscribePayload));
});

ws.on('message', async (message) => {
    console.log(message.toString());
    var parsedMessage = JSON.parse(message);
    switch (parsedMessage.channel) {
        case 'OBI':
            // ORDER BOOK INCREMENTAL
            if (localBookSnapshot === undefined) {
                // fetch snapshot the first time
                localBookSnapshot = await getBook("BTC-EUR", 100);
                console.log("Initial book: ", localBookSnapshot.sequence_number);
                break;
            }
            if (parsedMessage.data.length != 5) {
                console.log("invalid data: ", parsedMessage.data);
                break;
            }
            let bookUpdates = bookArrayToObject(parsedMessage.data);

            // check if the update is the next sequence number
            if (bookUpdates.sequence_number === localBookSnapshot.sequence_number + 1) {
                let buyKeys = Object.keys(bookUpdates.buys);
                let sellKeys = Object.keys(bookUpdates.sells);
                for (let i = 0; i < buyKeys.length; i++) {
                    let key = buyKeys[i];
                    if (bookUpdates.buys[key] === 0) {
                        // delete if volume is 0
                        delete localBookSnapshot.buys[key];
                    } else {
                        // update price point
                        localBookSnapshot.buys[key] = bookUpdates.buys[key];
                    }
                }
                for (let i = 0; i < sellKeys.length; i++) {
                    if (bookUpdates.sells[sellKeys[i]] === 0) {
                        delete localBookSnapshot.sells[sellKeys[i]];
                    } else {
                        localBookSnapshot.sells[sellKeys[i]] = bookUpdates.sells[sellKeys[i]];
                    }
                }
                //console.log("apply book updates " + bookUpdates.sequence_number +  " " + localBookSnapshot.sequence_number);
                localBookSnapshot.sequence_number = bookUpdates.sequence_number;

                // print best bid and ask first 5 depth
                let bestBid = Object.keys(localBookSnapshot.buys).sort((a, b) => b - a);
                let bestAsk = Object.keys(localBookSnapshot.sells).sort((a, b) => a - b);

                console.log("asks");
                for (let i = 4; i >= 0; i--) {
                    console.log(bestAsk[i], localBookSnapshot.sells[bestAsk[i]]);
                }
                console.log("bids");
                for (let i = 0; i < 5; i++) {
                    console.log(bestBid[i], localBookSnapshot.buys[bestBid[i]]);
                }
                console.log();
            } else {
                console.log("skip book update:" + bookUpdates.sequence_number);
            }
            break;
        default:
            console.log('Unknown channel: ', parsedMessage.channel, message.toString());
    }
});

ws.on('close', (code, reason) => {
    console.log('Disconnected from the WSS server.', code, reason.toJSON());
});

ws.on('error', (error) => {
    console.error(`WebSocket error: ${error.message}`);
});

async function getBook(pair, levels = 50) {
    try {
        let url = `${apiUrl}/api/v3/orderbook/${pair}/snapshot?levels=${levels}`;
        var data = (await axios.get(url)).data;
        return bookArrayToObject(data);
    } catch (e) {
        console.log(e);
        throw e;
    }
}

function bookArrayToObject(data) {
    var ret = {
        pair: data[0],
        buys: data[1].reduce((acc, x) => { acc[x[0]] = x[1]; return acc; }, {}),
        sells: data[2].reduce((acc, x) => { acc[x[0]] = x[1]; return acc; }, {}),
        sequence_number: data[3],
        timestamp: data[4]
    }
    return ret;
}

// const jwt = require('jsonwebtoken');
function generateJwt(apiKey, privateKey, payload) {
    let iat = Math.floor(Date.now() / 1000);
    let exp = iat + 30;
    if (payload == undefined) {
        // if GET request or no payload, use empty string
        payload = "";
    }
    let hashPayload = crypto.createHash('sha256').update(payload).digest('hex');
    const jwtClaims = {
        "sub": apiKey,
        "iat": iat,
        "exp": exp,
        "hash_payload": hashPayload
    };
    // quella che ti da API
    let privateKeyDer = "MHcCAQEEIB4rwBntv22TuFM0oyg0scEHxmodC2PYpFLOu8xeXl4goAoGCCqGSM49AwEHoUQDQgAEcqvovoSoDSXR9tilQNy77KNkXzAA70L7Je9GLogq3nCgDyboFMRp30/8a9UXeHLETG2JcstL9CHDCbCL8LFOhw==";

    let base64Key = Buffer.from(privateKeyDer, 'base64');
    const key = crypto.createPrivateKey( { key: base64Key, format: 'der', type: 'sec1' } );
    // const privkeyInPemFormat = key.export( { format: 'pem', type: 'sec1' } );
    var token = jwt.sign(jwtClaims, key, { algorithm: 'ES256' });
   return token;
}