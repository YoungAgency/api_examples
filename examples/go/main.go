package main

import "flag"

var example = ""

func init() {
	flag.StringVar(&example, "example", "v4", "Run a specific example, v4 | orderbook")
	flag.Parse()
}

func main() {
	switch example {
	case "v4":
		apiV4()
	case "orderbook":
		orderbook()
	}
}
