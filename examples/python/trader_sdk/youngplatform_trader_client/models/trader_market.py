from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.trader_market_details import TraderMarketDetails


T = TypeVar("T", bound="TraderMarket")


@_attrs_define
class TraderMarket:
    """
    Attributes:
        market (str | Unset): Market symbol in BASE-QUOTE format. Example: BTC-EUR.
        sor_details (TraderMarketDetails | Unset):
    """

    market: str | Unset = UNSET
    sor_details: TraderMarketDetails | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        market = self.market

        sor_details: dict[str, Any] | Unset = UNSET
        if not isinstance(self.sor_details, Unset):
            sor_details = self.sor_details.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if market is not UNSET:
            field_dict["market"] = market
        if sor_details is not UNSET:
            field_dict["sor_details"] = sor_details

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.trader_market_details import TraderMarketDetails

        d = dict(src_dict)
        market = d.pop("market", UNSET)

        _sor_details = d.pop("sor_details", UNSET)
        sor_details: TraderMarketDetails | Unset
        if isinstance(_sor_details, Unset):
            sor_details = UNSET
        else:
            sor_details = TraderMarketDetails.from_dict(_sor_details)

        trader_market = cls(
            market=market,
            sor_details=sor_details,
        )

        trader_market.additional_properties = d
        return trader_market

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
