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
            "currency": "1INCH",
            "balance": 0.0,
            "balanceInTrade": 0.0
        },
        {
            "currency": "AAVE",
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
You will receive order updates on this channel when
- order is matched
- order is closed
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
                "OrderID": 1697189430248568546,
                "CurrencyType": "BTC",
                "MarketType": "EUR",
                "OrderConfirmDate": "2023-10-13T09:30:30.248Z",
                "Volume": 0.00050000,
                "Rate": 25357.20000000,
                "ExecutionType": "SELL"
            },
            {
                "OrderID": 1697188785077629653,
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

# OrderBook Update
```json
{
    "status": "success",
    "channel": "OB",
    "data": {
        "pair": "BTC-EUR",
        "updates": {
            "bids": {
                "inserted": [
                    [
                        33084.15000000,
                        0.01345200
                    ]
                ],
                "removed": [
                    [
                        33084.17000000,
                        0.0
                    ]
                ],
                "changed": [
                    [
                        33085.15000000,
                        0.01449700
                    ]
                ]
            },
            "asks": {
                "inserted": [
                    [
                        33187.82000000,
                        0.02850000
                    ]
                ],
                "removed": [],
                "changed": []
            }
        }
    }
}
```


# OrderBook Incremental
New stream with sequence number
- connect to socket and buffer events
- use `/api/v3/orderbook/:pair/snapshot?levels=50` to get the current orderbook snapshot
- first socket event must have `sn = snapshot_sn + 1`
- process incremental updates
```json
{
    "status": "success",
    "channel": "OBI",
    "data": [
        "BTC_EUR", // pair
        [ // buys
            [
                40000.0,
                3.0,
                2 // update
            ],
            [
                39990.0,
                3.0,
                1 // insert
            ],
        ],
        [ // sells
            [
                41000.0,
                0.0,
                3 // delete
            ]
        ],
        747, // sequence number
        1705782984348 // timestamp
    ]
}
````
