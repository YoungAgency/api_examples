from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.trader_book_level import TraderBookLevel


T = TypeVar("T", bound="TraderBookResponse")


@_attrs_define
class TraderBookResponse:
    """
    Attributes:
        asks (list[TraderBookLevel] | Unset): Sell-side liquidity levels, best (lowest) price first.
        bids (list[TraderBookLevel] | Unset): Buy-side liquidity levels, best (highest) price first.
        market (str | Unset): Market symbol in BASE-QUOTE format. Example: BTC-EUR.
        mid_price (str | Unset): Midpoint between the best bid and best ask ("0" when the book is empty).
        time (str | Unset): Time the liquidity snapshot was taken.
    """

    asks: list[TraderBookLevel] | Unset = UNSET
    bids: list[TraderBookLevel] | Unset = UNSET
    market: str | Unset = UNSET
    mid_price: str | Unset = UNSET
    time: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        asks: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.asks, Unset):
            asks = []
            for asks_item_data in self.asks:
                asks_item = asks_item_data.to_dict()
                asks.append(asks_item)

        bids: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.bids, Unset):
            bids = []
            for bids_item_data in self.bids:
                bids_item = bids_item_data.to_dict()
                bids.append(bids_item)

        market = self.market

        mid_price = self.mid_price

        time = self.time

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if asks is not UNSET:
            field_dict["asks"] = asks
        if bids is not UNSET:
            field_dict["bids"] = bids
        if market is not UNSET:
            field_dict["market"] = market
        if mid_price is not UNSET:
            field_dict["mid_price"] = mid_price
        if time is not UNSET:
            field_dict["time"] = time

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.trader_book_level import TraderBookLevel

        d = dict(src_dict)
        _asks = d.pop("asks", UNSET)
        asks: list[TraderBookLevel] | Unset = UNSET
        if _asks is not UNSET:
            asks = []
            for asks_item_data in _asks:
                asks_item = TraderBookLevel.from_dict(asks_item_data)

                asks.append(asks_item)

        _bids = d.pop("bids", UNSET)
        bids: list[TraderBookLevel] | Unset = UNSET
        if _bids is not UNSET:
            bids = []
            for bids_item_data in _bids:
                bids_item = TraderBookLevel.from_dict(bids_item_data)

                bids.append(bids_item)

        market = d.pop("market", UNSET)

        mid_price = d.pop("mid_price", UNSET)

        time = d.pop("time", UNSET)

        trader_book_response = cls(
            asks=asks,
            bids=bids,
            market=market,
            mid_price=mid_price,
            time=time,
        )

        trader_book_response.additional_properties = d
        return trader_book_response

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
