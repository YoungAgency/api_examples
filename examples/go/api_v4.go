package main

import (
	"bytes"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"net/http"
	"time"

	jwt "github.com/golang-jwt/jwt/v5"
)

func main() {
	keyID := ""
	publicKey := ""
	privateKey := ""
	baseUrl := "https://api.youngplatform.com"

	balanceUrl := baseUrl + "/api/v4/private/balances"
	req, err := http.NewRequest("GET", balanceUrl, nil)
	if err != nil {
		panic(err)
	}
	jwt, err := generateJwt(publicKey, privateKey, []byte(""))
	if err != nil {
		panic(err)
	}
	req.Header.Add("Authorization", jwt)
	req.Header.Add("X-Api-Key-Id", keyID)

	res, err := http.DefaultClient.Do(req)
	if err != nil {
		panic(err)
	}
	defer res.Body.Close()

	if res.StatusCode != 200 {
		fmt.Println("Invalid status code", res.StatusCode)
		return
	}

	bodyBal := make([]map[string]interface{}, 0)

	if err := json.NewDecoder(res.Body).Decode(&bodyBal); err != nil {
		panic(err)
	}
	fmt.Println(bodyBal)

	// cancel order

	bodyCancel := map[string]interface{}{
		"orderId": 1,
	}
	bodyCancelBytes, err := json.Marshal(bodyCancel)
	if err != nil {
		panic(err)
	}

	urlCancel := baseUrl + "/api/v4/private/cancel"
	reqCancel, err := http.NewRequest("POST", urlCancel, bytes.NewBuffer(bodyCancelBytes))
	if err != nil {
		panic(err)
	}
	jwtCancel, err := generateJwt(publicKey, privateKey, bodyCancelBytes)
	if err != nil {
		panic(err)
	}
	reqCancel.Header.Add("Authorization", jwtCancel)
	reqCancel.Header.Add("X-Api-Key-Id", keyID)
	reqCancel.Header.Add("Content-Type", "application/json")

	resCancel, err := http.DefaultClient.Do(reqCancel)
	if err != nil {
		panic(err)
	}
	defer resCancel.Body.Close()

	bodyCancelRes := make(map[string]interface{})
	if err := json.NewDecoder(resCancel.Body).Decode(&bodyCancelRes); err != nil {
		panic(err)
	}
	fmt.Println(bodyCancelRes)
}

func generateJwt(publicKey string, privateKey string, body []byte) (string, error) {
	hasher := sha256.New()
	hasher.Write(body)
	hashBytes := hasher.Sum(nil)
	hashString := hex.EncodeToString(hashBytes)

	currentTs := time.Now().Unix()
	exp := currentTs + 10
	claims := jwt.MapClaims{
		"sub":          publicKey,
		"iat":          currentTs,
		"exp":          exp,
		"hash_payload": hashString,
	}
	jwtBuilder := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	token, err := jwtBuilder.SignedString([]byte(privateKey))
	if err != nil {
		return "", err
	}
	return token, nil
}
