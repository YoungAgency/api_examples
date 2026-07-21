from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Ticker")


@_attrs_define
class Ticker:
    """
    Attributes:
        amt (str | Unset): Traded amount over the window, in quote currency.
        c (str | Unset): Last price, in quote currency.
        h (str | Unset): Highest price of the window, in quote currency.
        l (str | Unset): Lowest price of the window, in quote currency.
        mkt (str | Unset): Market symbol in BASE-QUOTE format. Example: BTC-EUR.
        o (str | Unset): Opening price of the window, in quote currency.
        qty (str | Unset): Traded quantity over the window, in base currency.
        t (int | Unset): Snapshot time as Unix epoch milliseconds.
    """

    amt: str | Unset = UNSET
    c: str | Unset = UNSET
    h: str | Unset = UNSET
    l: str | Unset = UNSET
    mkt: str | Unset = UNSET
    o: str | Unset = UNSET
    qty: str | Unset = UNSET
    t: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        amt = self.amt

        c = self.c

        h = self.h

        l = self.l

        mkt = self.mkt

        o = self.o

        qty = self.qty

        t = self.t

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if amt is not UNSET:
            field_dict["amt"] = amt
        if c is not UNSET:
            field_dict["c"] = c
        if h is not UNSET:
            field_dict["h"] = h
        if l is not UNSET:
            field_dict["l"] = l
        if mkt is not UNSET:
            field_dict["mkt"] = mkt
        if o is not UNSET:
            field_dict["o"] = o
        if qty is not UNSET:
            field_dict["qty"] = qty
        if t is not UNSET:
            field_dict["t"] = t

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        amt = d.pop("amt", UNSET)

        c = d.pop("c", UNSET)

        h = d.pop("h", UNSET)

        l = d.pop("l", UNSET)

        mkt = d.pop("mkt", UNSET)

        o = d.pop("o", UNSET)

        qty = d.pop("qty", UNSET)

        t = d.pop("t", UNSET)

        ticker = cls(
            amt=amt,
            c=c,
            h=h,
            l=l,
            mkt=mkt,
            o=o,
            qty=qty,
            t=t,
        )

        ticker.additional_properties = d
        return ticker

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
