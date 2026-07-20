from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ohlc_candle import OhlcCandle


T = TypeVar("T", bound="TraderCharts")


@_attrs_define
class TraderCharts:
    """
    Attributes:
        candles (list[OhlcCandle] | Unset): OHLC candles, most recent first.
    """

    candles: list[OhlcCandle] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        candles: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.candles, Unset):
            candles = []
            for candles_item_data in self.candles:
                candles_item = candles_item_data.to_dict()
                candles.append(candles_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if candles is not UNSET:
            field_dict["candles"] = candles

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ohlc_candle import OhlcCandle

        d = dict(src_dict)
        _candles = d.pop("candles", UNSET)
        candles: list[OhlcCandle] | Unset = UNSET
        if _candles is not UNSET:
            candles = []
            for candles_item_data in _candles:
                candles_item = OhlcCandle.from_dict(candles_item_data)

                candles.append(candles_item)

        trader_charts = cls(
            candles=candles,
        )

        trader_charts.additional_properties = d
        return trader_charts

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
