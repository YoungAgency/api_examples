const WebSocket = require('ws');
const axios = require('axios');

const wssURL = 'wss://api.youngplatform.com/ws';
const apiUrl = 'https://api.youngplatform.com';

const ws = new WebSocket(wssURL);

var localBookSnapshot = undefined;

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