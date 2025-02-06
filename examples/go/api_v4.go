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

const baseURL = "https://api.youngplatform.com"

// Configuration
var (
	keyID      = "" // Replace with your key ID
	publicKey  = "" // Replace with your public key
	privateKey = "" // Replace with your private key
)

func apiV4() {
	if keyID == "" || publicKey == "" || privateKey == "" {
		panic("Please set keyID, publicKey, and privateKey")
	}

	// Retrieve balance
	balances, err := getBalances()
	if err != nil {
		fmt.Printf("Error retrieving balances: %v\n", err)
		return
	}
	fmt.Println("Balances:", balances)

	// Cancel an order
	orderID := 1
	cancelResponse, err := cancelOrder(orderID)
	if err != nil {
		fmt.Printf("Error cancelling order: %v\n", err)
		return
	}
	fmt.Println("Cancel response:", cancelResponse)
}

func getBalances() ([]map[string]interface{}, error) {
	url := baseURL + "/api/v4/private/balances"

	req, err := http.NewRequest("GET", url, nil)
	if err != nil {
		return nil, err
	}

	token, err := generateJwt(publicKey, privateKey, nil)
	if err != nil {
		return nil, err
	}

	req.Header.Set("Authorization", token)
	req.Header.Set("X-Api-Key-Id", keyID)

	res, err := http.DefaultClient.Do(req)
	if err != nil {
		return nil, err
	}
	defer res.Body.Close()

	if res.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("unexpected status code: %d", res.StatusCode)
	}

	var balances []map[string]interface{}
	if err := json.NewDecoder(res.Body).Decode(&balances); err != nil {
		return nil, err
	}

	return balances, nil
}

func cancelOrder(orderID int) (map[string]interface{}, error) {
	url := baseURL + "/api/v4/private/cancel"

	body := map[string]interface{}{
		"orderId": orderID,
	}
	bodyBytes, err := json.Marshal(body)
	if err != nil {
		return nil, err
	}

	req, err := http.NewRequest("POST", url, bytes.NewBuffer(bodyBytes))
	if err != nil {
		return nil, err
	}

	token, err := generateJwt(publicKey, privateKey, bodyBytes)
	if err != nil {
		return nil, err
	}

	req.Header.Set("Authorization", token)
	req.Header.Set("X-Api-Key-Id", keyID)
	req.Header.Set("Content-Type", "application/json")

	res, err := http.DefaultClient.Do(req)
	if err != nil {
		return nil, err
	}
	defer res.Body.Close()

	var response map[string]interface{}
	if err := json.NewDecoder(res.Body).Decode(&response); err != nil {
		return nil, err
	}

	return response, nil
}

func generateJwt(publicKey, privateKey string, body []byte) (string, error) {
	hasher := sha256.New()
	hasher.Write(body)
	hashString := hex.EncodeToString(hasher.Sum(nil))

	now := time.Now().Unix()
	claims := jwt.MapClaims{
		"sub":          publicKey,
		"iat":          now,
		"exp":          now + 30, // Token expires in 30 seconds
		"hash_payload": hashString,
	}

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	signedToken, err := token.SignedString([]byte(privateKey))
	if err != nil {
		return "", err
	}

	return signedToken, nil
}
