from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="OhlcCandle")


@_attrs_define
class OhlcCandle:
    """
    Attributes:
        close (str | Unset): Closing price of the candle, in quote currency.
        close_at (str | Unset): End of the candle window.
        high (str | Unset): Highest price of the candle, in quote currency.
        low (str | Unset): Lowest price of the candle, in quote currency.
        market (str | Unset): Market symbol in BASE-QUOTE format. Example: BTC-EUR.
        open_ (str | Unset): Opening price of the candle, in quote currency.
        open_at (str | Unset): Start of the candle window (inclusive).
        rfq_amount (str | Unset): RFQ traded amount in quote currency.
        rfq_volume (str | Unset): RFQ traded volume in base currency.
        sor_amount (str | Unset): SOR traded amount in quote currency.
        sor_volume (str | Unset): SOR traded volume in base currency.
    """

    close: str | Unset = UNSET
    close_at: str | Unset = UNSET
    high: str | Unset = UNSET
    low: str | Unset = UNSET
    market: str | Unset = UNSET
    open_: str | Unset = UNSET
    open_at: str | Unset = UNSET
    rfq_amount: str | Unset = UNSET
    rfq_volume: str | Unset = UNSET
    sor_amount: str | Unset = UNSET
    sor_volume: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        close = self.close

        close_at = self.close_at

        high = self.high

        low = self.low

        market = self.market

        open_ = self.open_

        open_at = self.open_at

        rfq_amount = self.rfq_amount

        rfq_volume = self.rfq_volume

        sor_amount = self.sor_amount

        sor_volume = self.sor_volume

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if close is not UNSET:
            field_dict["close"] = close
        if close_at is not UNSET:
            field_dict["close_at"] = close_at
        if high is not UNSET:
            field_dict["high"] = high
        if low is not UNSET:
            field_dict["low"] = low
        if market is not UNSET:
            field_dict["market"] = market
        if open_ is not UNSET:
            field_dict["open"] = open_
        if open_at is not UNSET:
            field_dict["open_at"] = open_at
        if rfq_amount is not UNSET:
            field_dict["rfq_amount"] = rfq_amount
        if rfq_volume is not UNSET:
            field_dict["rfq_volume"] = rfq_volume
        if sor_amount is not UNSET:
            field_dict["sor_amount"] = sor_amount
        if sor_volume is not UNSET:
            field_dict["sor_volume"] = sor_volume

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        close = d.pop("close", UNSET)

        close_at = d.pop("close_at", UNSET)

        high = d.pop("high", UNSET)

        low = d.pop("low", UNSET)

        market = d.pop("market", UNSET)

        open_ = d.pop("open", UNSET)

        open_at = d.pop("open_at", UNSET)

        rfq_amount = d.pop("rfq_amount", UNSET)

        rfq_volume = d.pop("rfq_volume", UNSET)

        sor_amount = d.pop("sor_amount", UNSET)

        sor_volume = d.pop("sor_volume", UNSET)

        ohlc_candle = cls(
            close=close,
            close_at=close_at,
            high=high,
            low=low,
            market=market,
            open_=open_,
            open_at=open_at,
            rfq_amount=rfq_amount,
            rfq_volume=rfq_volume,
            sor_amount=sor_amount,
            sor_volume=sor_volume,
        )

        ohlc_candle.additional_properties = d
        return ohlc_candle

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
