# Youngplatform API Examples

[Postman Documentation](https://documenter.getpostman.com/view/20237880/2sAYJAdxQv)

This repository provides some examples for connection to Youngplatform APIs.

JWT examples provides examples of JWT generation for authenticated requests.
 
- [Python REST API JWT](./examples/python/api_v4.py)
- [Node REST API JWT](./examples/js/api_v4.js)
- [Go REST API JWT](./examples/go/api_v4.go)
- [Python Socket](./examples/python/socket_connect.py)
- [Node Socket](./examples/js/socket_connect.js)
- [Node OBI implementation](./examples/js/socket_orderbook_snapshot.js)
- [Go OBI implementation](./examples/go/socket_orderbook_snapshot.go)


## Authentication

To authenticate, include the following headers in your initial HTTP request:  
- **`Authorization`**: The access token.  
- **`X-Api-Key-Id`**: The corresponding API key ID.

### JWT Authentication

Access to private APIs, both on REST and WebSocket endpoints, requires a **JWT token**.

You need to generate Api Keys at pro.youngplatform.com

To successfully authenticate, you need the following credentials:  
- **KEY_ID**  
- **PUBLIC_KEY**  
- **PRIVATE_KEY**  

This repository provides examples of generating JWT tokens in both JavaScript and Python.

#### JWT Payload
The `Payload` can be one of the following:  
- An empty string (`""`) for **GET requests** or **WebSocket login**.  
- The **SHA-256 hash** of the request payload string for other requests.

The following snippet demonstrates how to generate a JWT token in JavaScript:


```js
let token = generateJwt(PUBLIC_KEY, PRIVTE_KEY);
let headers ={ "Authorization": token, "X-Api-Key-Id": KEY_ID}
var data = (await axios.get(url, { headers: headers })).data;

function generateJwt(publicKey, privateKey, payload) {
    let iat = Math.floor(Date.now() / 1000);
    let exp = iat + 30;
    if (payload == undefined) {
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
```


# Socket

There are four message types:

* `ping`: required to be sent once each 30 seconds, otherwise the client will be disconnected
* `subscribe`: used to subscribe to events, invalid events won't trigger any error response
* `unsubscribe`: used to unsubscribe to events, invalid events won't trigger any error response
* `logout`: closes the connection


- Multiple subscribtions can be requested with a single subscribe message.
- Some requires authentication (marked).
- Some will send an initial snapshot of the requested data.

## Ticker (snapshot)
You will receive ticker updates for a specific pair's ticker

### Subscribe message
```json
{
    "ID": "1",
    "method": "subscribe",
    "events": [
        "T.BTC-EUR"
    ]
}
```

### Updates
```json
{
    "type": "T.BTC-EUR",
    "data": {
        "b": "BTC",        // base currency
        "q": "EUR",        // quote currency
        "o": "99000.00",   // open price
        "h": "101000.00",  // high price
        "l": "97000.00",   // low price
        "c": "98000.00",   // close price
        "v": "2.00",       // volume in BASE currency
        "t": 1736876837081 // timestamp
    }
}
```


## Trade history
You will receive public trades of a specific pair

### Subcribe message
```json
{
    "ID": "1",
    "method": "subscribe",
    "events": [
        "TH.BTC-EUR"
    ]
}
```

### Updates
```json
{
    "type": "TH.BTC-EUR",
    "data": {
        "i": 123456,       // trade id
        "b": "BTC",        // base currency
        "q": "EUR",        // quote currency
        "v": "0.3",        // volume
        "r": "98481.12",   // rate
        "s": "BUY",        // execution side
        "t": 1736876837381 // timestamp
    }
}
```

## Private Trades (authenticated)

Source: Memory

You will receive private trade execution messages on this channel.

This subscription is faster than Private Orders (PO)

### Subscribe message
```json
{
    "ID": "1",
    "method": "subscribe",
    "events": [
        "TP.BTC-EUR"
    ]
}
```

## Updates
The update message will contain either buy order id (`bi`) or sell order id (`si`)

```json
{
    "type": "TP.BTC-EUR",
    "data": {
        "ts": 1736876837381, // timestamp
        "b": "BTC",          // base currency
        "q": "EUR",          // quote currency
        "v": "0.3",          // volume
        "r": "98481.12",     // rate
        "s": "BUY",          // execution side
        "a": "29544.336",    // amount
        "f": "0.0003",       // fee
        "i": 123456,         // match order id
        "bi": 88481001,      // buy order id
        "si": 88481001,      // sell order id
    }
}
```

## Private Orders (authenticated, snapshot)

Source: Database

You will receive order updates on this channel when:
- order is placed
- order is matched
- order is closed


### Subscribe message
```json
{
    "ID": "1",
    "method": "subscribe",
    "events": [
        "PO.BTC-EUR"
    ]
}
```

### Updates
```json
{
    "type": "PO.BTC-EUR",
    "data": {
        "i": 123456789, // order id
        "c": 987654,
        "b": "BTC", // base
        "q": "EUR", // quote
        "v": "0.15000000", // volume 
        "r": "45000.00000000", // rate
        "sr": "46000.00000000", // stop rate
        "p": "0.05000000", // pending volume
        "ty": "LIMIT",
        "tif": "GTC",
        "s": "BUY",
        "coid": "client_order_123",
        "ts": 1705782984348, // order placed ms
        "a": "6750.00000000", // amount
        "f": "13.50000000", // fee (if buy in BASE else QUOTE)
        "mv": "0.10000000", // matched volume
        "ma": "4500.00000000", // matched amount
        "mr": "45000.00000000", // matched avg rate
        "cts": 1705783084348 // order closed ms
    }
}
```

# Balance updates (authenticated, snapshot)
This channel is used to receive balance updates for all currencies.
On connect, all balances are sent.

### Subscribe message
```json
{
    "ID": "1",
    "method": "subscribe",
    "events": [
        "BL"
    ]
}
```

### Updates
```json
{
  "type": "BL",
  "data": [
    {
        "c": "BTC",   // currency
        "b": "0.001", // balance
        "t": "0.002"    // balance in trade
    }
  ]
}
```


# OrderBook Incremental

- connect to OBI stream and buffer events
- make an HTTP GET request to the `/api/v4/public/orderbook?pair=${pair}&levels=${levels}`endpoint to fetch the current order book snapshot for the specified trading pair. This snapshot will provide the initial state of the order book.

- once the snapshot is received, ensure that the sequence number (sn) of the first event processed from the WebSocket stream is equal to the sn of the snapshot + 1. This ensures that you're starting with the correct sequence number for subsequent incremental updates.sn = snapshot_sn + 1

- continue listening to the WebSocket stream for incremental updates to the order book. Each update will have its own sequence number (sn). Verify that the sequence number of each incremental update is equal to the snapshot's sequence number plus one. If this condition is not met you must re-request the snapshot.


### Subscribe Message
```json
{
  "method": "subscribe",
  "events": ["OBI.BTC-EUR"]
}
```

### Updates
```json
{
  "type": "OBI.BTC-EUR",
  "data": [
    "BTC_EUR",
    [ // bids
      [
        "94980.33", // price
        "1",// volume
      ]
    ],
    [ // asks
      [
        "95361.01", // price
        "1" // volume
      ],
      [
        "95361.02",
        "0" // volume = 0 = deleted
      ]
    ],
    18042501, // sequence number
    1738008065894 // timestamp
  ]
}
````

