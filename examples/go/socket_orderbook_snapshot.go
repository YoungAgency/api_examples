package main

import (
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"slices"
	"strconv"
	"strings"

	"github.com/gorilla/websocket"
)

func orderbook() {

	orderbookCache, err := getOrderBook("BTC-EUR")
	if err != nil {
		panic(err)
	}

	for _, el := range orderbookCache.top5() {
		fmt.Println(el[0], el[1])
	}

	fmt.Println()

	for update := range socketUpdates("BTC-EUR") {
		if update.SequenceNumber == orderbookCache.SequenceNumber+1 {
			orderbookCache.ApplyUpdate(*update)
			for _, el := range orderbookCache.top5() {
				fmt.Println(el[0], el[1])
			}
			fmt.Println()
		} else {
			// TODO: should buffer events before requesting a new snapshot
			// TODO: handle errors
			panic("Invalid sequence number")
		}
	}
}

func socketUpdates(pair string) chan *orderBook {
	out := make(chan *orderBook)

	go func() {
		defer close(out)

		socket, resHttp, err := websocket.DefaultDialer.DialContext(context.Background(), "wss://api.youngplatform.com/api/socket/ws", nil)
		if err != nil {
			fmt.Println(resHttp)
			panic(err)
		}
		defer socket.Close()

		// subscribe to balance updates
		body := map[string]any{
			"method": "subscribe",
			"events": []string{"OBI." + pair},
		}

		if err := socket.WriteJSON(body); err != nil {
			panic(err)
		}

		for {
			_, msg, err := socket.ReadMessage()
			if err != nil {
				panic(err)
			}

			socketMessage := struct {
				Type string `json:"type"`
				Data any    `json:"data"`
			}{}
			if err := json.Unmarshal(msg, &socketMessage); err != nil {
				panic(err)
			}
			if strings.HasPrefix(socketMessage.Type, "OBI.") {
				ret := &orderBook{
					Buys:           make(map[float64]float64),
					Sells:          make(map[float64]float64),
					SequenceNumber: int64(socketMessage.Data.([]any)[3].(float64)),
				}
				buys := socketMessage.Data.([]any)[1]
				sells := socketMessage.Data.([]any)[2]

				for i := range buys.([]any) {
					buy := buys.([]any)[i].([]any)
					priceS := buy[0].(string)
					sizeS := buy[1].(string)

					price, _ := strconv.ParseFloat(priceS, 64)
					size, _ := strconv.ParseFloat(sizeS, 64)

					ret.Buys[price] = size
				}

				for i := range sells.([]any) {
					sell := sells.([]any)[i].([]any)
					priceS := sell[0].(string)
					sizeS := sell[1].(string)

					price, _ := strconv.ParseFloat(priceS, 64)
					size, _ := strconv.ParseFloat(sizeS, 64)
					ret.Sells[price] = size
				}
				out <- ret
			}

		}
	}()

	return out
}

func getOrderBook(pair string) (*orderBook, error) {
	url := fmt.Sprintf("https://api.youngplatform.com/api/v4/public/orderbook?pair=%s", pair)
	req, err := http.NewRequest("GET", url, nil)
	if err != nil {
		return nil, err
	}

	res, err := http.DefaultClient.Do(req)
	if err != nil {
		return nil, err
	}
	defer res.Body.Close()

	if res.StatusCode != 200 {
		return nil, fmt.Errorf("Invalid status code %d", res.StatusCode)
	}

	ob := struct {
		Buys []struct {
			Price float64 `json:"price"`
			Size  float64 `json:"size"`
		}
		Sells []struct {
			Price float64 `json:"price"`
			Size  float64 `json:"size"`
		}
		SequenceNumber int64 `json:"sequenceNumber"`
	}{}
	if err := json.NewDecoder(res.Body).Decode(&ob); err != nil {
		return nil, err
	}

	ret := orderBook{
		Buys:           make(map[float64]float64),
		Sells:          make(map[float64]float64),
		SequenceNumber: ob.SequenceNumber,
	}

	for _, buy := range ob.Buys {
		ret.Buys[buy.Price] = buy.Size
	}
	for _, sell := range ob.Sells {
		ret.Sells[sell.Price] = sell.Size
	}

	return &ret, nil
}

type orderBook struct {
	Buys           map[float64]float64 `json:"buys"`
	Sells          map[float64]float64 `json:"sells"`
	SequenceNumber int64               `json:"sequenceNumber"`
}

func (ob *orderBook) ApplyUpdate(u orderBook) {
	ob.SequenceNumber = u.SequenceNumber

	for price, size := range u.Buys {
		if size == 0 {
			delete(ob.Buys, price)
		} else {
			ob.Buys[price] = size
		}
	}
	for price, size := range u.Sells {
		if size == 0 {
			delete(ob.Sells, price)
		} else {
			ob.Sells[price] = size
		}
	}
}

func (ob *orderBook) top5() [][]float64 {
	buys := make([][]float64, 0)
	sells := make([][]float64, 0)

	for price, size := range ob.Buys {
		buys = append(buys, []float64{price, size})
	}
	for price, size := range ob.Sells {
		sells = append(sells, []float64{price, size})
	}

	slices.SortFunc(buys, func(a, b []float64) int {
		if a[0] < b[0] {
			return 1
		}
		if a[0] > b[0] {
			return -1
		}
		return 0
	})

	slices.SortFunc(sells, func(a, b []float64) int {
		if a[0] < b[0] {
			return -1
		}
		if a[0] > b[0] {
			return 1
		}
		return 0
	})

	ret := make([][]float64, 0)

	sells = sells[:5]
	buys = buys[:5]
	for i := 0; i < 5; i++ {
		if i < len(sells) {
			ret = append(ret, sells[len(sells)-1-i])
		}
	}

	ret = append(ret, []float64{0, 0})

	for i := 0; i < 5; i++ {
		if i < len(buys) {
			ret = append(ret, buys[i])
		}
	}
	return ret
}
