from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ticker import Ticker


T = TypeVar("T", bound="TraderTickers")


@_attrs_define
class TraderTickers:
    """
    Attributes:
        tickers (list[Ticker] | Unset): One ticker snapshot per market.
    """

    tickers: list[Ticker] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        tickers: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.tickers, Unset):
            tickers = []
            for tickers_item_data in self.tickers:
                tickers_item = tickers_item_data.to_dict()
                tickers.append(tickers_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if tickers is not UNSET:
            field_dict["tickers"] = tickers

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ticker import Ticker

        d = dict(src_dict)
        _tickers = d.pop("tickers", UNSET)
        tickers: list[Ticker] | Unset = UNSET
        if _tickers is not UNSET:
            tickers = []
            for tickers_item_data in _tickers:
                tickers_item = Ticker.from_dict(tickers_item_data)

                tickers.append(tickers_item)

        trader_tickers = cls(
            tickers=tickers,
        )

        trader_tickers.additional_properties = d
        return trader_tickers

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
