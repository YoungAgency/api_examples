# Websocket API

```sh
export YOUNG_API_SECRET=foobar
export YOUNG_API_KEY=foobar
cd socket/js
npm install
node index.js 
```

# OrderBook Incremental

- make an HTTP GET request to the `/api/v4/public/orderbook/?pair=${pair}&levels=${levels}` endpoint to fetch the current order book snapshot for the specified trading pair. This snapshot will provide the initial state of the order book.

- once the snapshot is received, process it accordingly. Ensure that the sequence number (sn) of the first event processed from the WebSocket stream is equal to the sn of the snapshot plus one. This ensures that you're starting with the correct sequence number for subsequent incremental updates.`sn = snapshot_sn + 1`

- after processing the snapshot, continue listening to the WebSocket stream for incremental updates to the order book. Each update will have its own sequence number (sn). Verify that the sequence number of each incremental update is equal to the snapshot's sequence number plus one. If this condition is not met you must re-request the snapshot.

### Payload
```json
{
    "method": "subscribe",
    "events": ["OBI.BTC-EUR"]
}
```

### Event
```json
{
    "status": "success",
    "channel": "OBI",
    "data": [
        "BTC_EUR", // pair
        [ // buys
            [
                40000.0,
                3.0
            ],
            [
                39990.0,
                3.0
            ],
        ],
        [ // sells
            [
                41000.0,
                0.0
            ]
        ],
        747, // sequence number
        1705782984348 // timestamp
    ]
}
````
