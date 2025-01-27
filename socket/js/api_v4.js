const axios = require('axios');
const crypto = require('crypto');
const jwt = require('jsonwebtoken');

const keyId = "";
const publicKey = "";
const privateKey = "";
const apiUrl = 'https://api.youngplatform.com';

getBalance().then((data) => {
    console.log(data);
    return cancelOrder("1");
})
.then((data) => {
    console.log(data);
})
.catch((e) => {
    console.log(e);
});

async function getBalance() {
    try {
        let url = `${apiUrl}/api/v4/private/balances`;
        let token = generateJwt(publicKey, privateKey, "");
        let headers ={
            "Authorization": token,
            "X-Api-Key-Id": keyId,
        }
        var data = (await axios.get(url, { headers: headers })).data;
        return data;
    } catch (e) {
        console.log(e);
        throw e;
    }
}

async function cancelOrder(orderId) {
    try {
        let url = `${apiUrl}/api/v4/private/cancel`;
        let body = {
            "orderId": orderId
        }
        let bodyString = JSON.stringify(body);
        let token = generateJwt(publicKey, privateKey, bodyString);
        let headers ={
            "Authorization": token,
            "X-Api-Key-Id": keyId,
            "Content-Type": "application/json"
        }
        var data = (await axios.post(url, bodyString, {headers: headers})).data;
        return data;
    }
    catch (e) {
        if (e.response.status == 400) {
            return e.response.data;
        }
        throw e;
    }
}


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