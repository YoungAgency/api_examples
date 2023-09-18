# Websocket API

```sh
cd socket/js
npm install
node index.js 
```

## Balances (BAL)
You will receive a list of all balances on this channel when you connect to the websocket.
You will receive updates on this channel when balance is updated.
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


# Order Update (PO)
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