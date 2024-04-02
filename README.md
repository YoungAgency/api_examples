# Websocket API

```sh
export YOUNG_API_SECRET=foobar
export YOUNG_API_KEY=foobar
cd socket/js
npm install
node index.js 
```

## Balances (BAL)
You will receive:
- a list of all balances on this channel when you connect to the websocket.
- object when balance is updated
### First message
```json
{
    "status": "success",
    "channel": "BAL",
    "data": [
        {
            "currency": "BTC",
            "balance": 0.0,
            "balanceInTrade": 0.0
        },
        {
            "currency": "EUR",
            "balance": 0.0,
            "balanceInTrade": 0.0
        }
    ]
}
```

### Updates
```json
{
    "status": "success",
    "channel": "BAL",
    "data": {
        "currency": "1INCH",
        "balance": 0.0,
        "balanceInTrade": 0.0
    }
}
```


# Order Update (OU)
You will receive order updates on this channel when:
- order is matched
- order is closed

### Payload
```json
{
    "op": "SUBSCRIBE",
    "channel": "OU",
    "data": {
        "pairs": ["BTC-EUR"]
    }
}
```

### Event
```json
{
    "status": "success",
    "channel": "OU",
    "data": {
        "orderID": 3170140763,
        "base": "BTC",
        "quote": "EUR",
        "volume": 0.20000000,
        "pendingVolume": 0.20000000, // 0 when order fully matched
        "rate": 30000.00000000,
        "status": false,
        "category": "LIMIT",
        "tif": "GTC",
        "side": "SELL",
        "placementDate": "2023-09-18T12:56:02.8437594Z",
        "confirmDate": null, // not null when closed
        "stop": 0.0,
        "isProOrder": false
    }
}
```

# Public Trades
```json
{
    "status": "success",
    "channel": "PT",
    "data": {
        "pair": "BTC-EUR",
        "trades": [
            {
                "OrderID": 1697189546,
                "CurrencyType": "BTC",
                "MarketType": "EUR",
                "OrderConfirmDate": "2023-10-13T09:30:30.248Z",
                "Volume": 0.00050000,
                "Rate": 25357.20000000,
                "ExecutionType": "SELL"
            },
            {
                "OrderID": 1697629653,
                "CurrencyType": "BTC",
                "MarketType": "EUR",
                "OrderConfirmDate": "2023-10-13T09:19:45.077Z",
                "Volume": 0.00039000,
                "Rate": 25503.27000000,
                "ExecutionType": "BUY"
            }
        ]
    }
}
```

# OrderBook Incremental

- make an HTTP GET request to the `/api/v3/orderbook/:pair/snapshot?levels=50` endpoint to fetch the current order book snapshot for the specified trading pair. This snapshot will provide the initial state of the order book.

- once the snapshot is received, process it accordingly. Ensure that the sequence number (sn) of the first event processed from the WebSocket stream is equal to the sn of the snapshot plus one. This ensures that you're starting with the correct sequence number for subsequent incremental updates.`sn = snapshot_sn + 1`

- after processing the snapshot, continue listening to the WebSocket stream for incremental updates to the order book. Each update will have its own sequence number (sn). Verify that the sequence number of each incremental update is equal to the snapshot's sequence number plus one. If this condition is not met you must re-request the snapshot.

### Payload
```json
{
    "op": "SUBSCRIBE",
    "channel": "OBI",
    "data": {
        "pairs": ["BTC-EUR"]
    }
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
