package main

import (
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"slices"
	"strconv"
	"strings"
	"time"

	"github.com/gorilla/websocket"
)

type orderBook struct {
	Buys           map[float64]float64
	Sells          map[float64]float64
	SequenceNumber int64
}

func orderbook() {
	var orderbookCache *orderBook
	// connect to socket
	for update := range socketUpdates("BTC-EUR") {
		if orderbookCache == nil {
			var err error
			// fetch snapshot
			orderbookCache, err = getOrderBook("BTC-EUR")
			if err != nil {
				panic(err)
			}
		}
		// ignore messages received before the snapshot
		if update.SequenceNumber <= orderbookCache.SequenceNumber {
			fmt.Println("Skipping update", update.SequenceNumber, orderbookCache.SequenceNumber)
			continue
		}
		if update.SequenceNumber == orderbookCache.SequenceNumber+1 {
			orderbookCache.ApplyUpdate(*update)
			orderbookCache.Print(5)
		} else {
			fmt.Println("Sequence number mismatch", orderbookCache.SequenceNumber, update.SequenceNumber)
			panic("Invalid sequence number")
		}
	}
}

func reduce(arr [][]float64) float64 {
	sum := 0.0
	for _, el := range arr {
		sum += el[0] * el[1]
	}
	return sum
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

				// create map of buys and sells using prices as keys
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
		Bids []struct {
			Rate   string `json:"r"`
			Volume string `json:"v"`
		} `json:"bids"`
		Asks []struct {
			Rate   string `json:"r"`
			Volume string `json:"v"`
		} `json:"asks"`
		SequenceNumber int64 `json:"sn"`
	}{}
	if err := json.NewDecoder(res.Body).Decode(&ob); err != nil {
		return nil, err
	}

	ret := orderBook{
		Buys:           make(map[float64]float64),
		Sells:          make(map[float64]float64),
		SequenceNumber: ob.SequenceNumber,
	}

	for _, buy := range ob.Bids {
		rateF, _ := strconv.ParseFloat(buy.Rate, 64)
		volumeF, _ := strconv.ParseFloat(buy.Volume, 64)
		ret.Buys[rateF] = volumeF
	}
	for _, sell := range ob.Asks {
		rateF, _ := strconv.ParseFloat(sell.Rate, 64)
		volumeF, _ := strconv.ParseFloat(sell.Volume, 64)
		ret.Sells[rateF] = volumeF
	}

	return &ret, nil
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

func (ob *orderBook) topN(n int) [][]float64 {
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

	sells = sells[:n]
	buys = buys[:n]
	for i := 0; i < n; i++ {
		if i < len(sells) {
			ret = append(ret, sells[len(sells)-1-i])
		}
	}

	for i := 0; i < n; i++ {
		if i < len(buys) {
			ret = append(ret, buys[i])
		}
	}
	return ret
}

func (ob *orderBook) Print(n int) {
	fmt.Println(ob.SequenceNumber, len(ob.Buys), len(ob.Sells), time.Now().UTC())
	data := ob.topN(n)
	sellCum := reduce(data[:n])
	buyCum := 0.0
	//   98084.24 | 0.000120 |      11.77 | 3651
	fmt.Println("  Price	   |  Size    |  Amount    | Cumulative")
	for i, el := range data {
		if el[0] == 0 {
			fmt.Println("----")
			continue
		}
		cumAmount := 0.0
		if i < len(data)/2 {
			cumAmount = sellCum
		} else {
			cumAmount = buyCum + el[0]*el[1]
		}
		if i == len(data)/2 {
			fmt.Println("  ----")
		}
		fmt.Printf("%10.2f | %2.6f | %10.2f | %2.f\n", el[0], el[1], el[0]*el[1], cumAmount)
		if i < len(data)/2 {
			sellCum -= el[0] * el[1]
		} else {
			buyCum += el[0] * el[1]
		}
	}
	fmt.Println()
	fmt.Println()
}
