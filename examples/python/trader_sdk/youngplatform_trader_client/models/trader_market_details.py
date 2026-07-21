from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TraderMarketDetails")


@_attrs_define
class TraderMarketDetails:
    """
    Attributes:
        active (bool | Unset): Whether the market is currently tradable at all.
        amount_precision (int | Unset): Maximum number of decimal places on amounts (quote currency).
        buy_enabled (bool | Unset): Whether buy orders are currently accepted.
        max_order_amount (float | Unset): Maximum order amount (quantity x price), in quote currency (0 = no cap).
        max_order_quantity (float | Unset): Maximum order quantity, in base currency (0 = no cap).
        min_order_amount (float | Unset): Minimum order amount (quantity x price), in quote currency.
        min_order_quantity (float | Unset): Minimum order quantity, in base currency.
        min_tick_size (float | Unset): Smallest price increment, in quote currency.
        price_precision (int | Unset): Maximum number of decimal places accepted on order price (quote currency).
        quantity_precision (int | Unset): Maximum number of decimal places accepted on order quantity (base currency).
        sell_enabled (bool | Unset): Whether sell orders are currently accepted.
    """

    active: bool | Unset = UNSET
    amount_precision: int | Unset = UNSET
    buy_enabled: bool | Unset = UNSET
    max_order_amount: float | Unset = UNSET
    max_order_quantity: float | Unset = UNSET
    min_order_amount: float | Unset = UNSET
    min_order_quantity: float | Unset = UNSET
    min_tick_size: float | Unset = UNSET
    price_precision: int | Unset = UNSET
    quantity_precision: int | Unset = UNSET
    sell_enabled: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        active = self.active

        amount_precision = self.amount_precision

        buy_enabled = self.buy_enabled

        max_order_amount = self.max_order_amount

        max_order_quantity = self.max_order_quantity

        min_order_amount = self.min_order_amount

        min_order_quantity = self.min_order_quantity

        min_tick_size = self.min_tick_size

        price_precision = self.price_precision

        quantity_precision = self.quantity_precision

        sell_enabled = self.sell_enabled

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if active is not UNSET:
            field_dict["active"] = active
        if amount_precision is not UNSET:
            field_dict["amount_precision"] = amount_precision
        if buy_enabled is not UNSET:
            field_dict["buy_enabled"] = buy_enabled
        if max_order_amount is not UNSET:
            field_dict["max_order_amount"] = max_order_amount
        if max_order_quantity is not UNSET:
            field_dict["max_order_quantity"] = max_order_quantity
        if min_order_amount is not UNSET:
            field_dict["min_order_amount"] = min_order_amount
        if min_order_quantity is not UNSET:
            field_dict["min_order_quantity"] = min_order_quantity
        if min_tick_size is not UNSET:
            field_dict["min_tick_size"] = min_tick_size
        if price_precision is not UNSET:
            field_dict["price_precision"] = price_precision
        if quantity_precision is not UNSET:
            field_dict["quantity_precision"] = quantity_precision
        if sell_enabled is not UNSET:
            field_dict["sell_enabled"] = sell_enabled

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        active = d.pop("active", UNSET)

        amount_precision = d.pop("amount_precision", UNSET)

        buy_enabled = d.pop("buy_enabled", UNSET)

        max_order_amount = d.pop("max_order_amount", UNSET)

        max_order_quantity = d.pop("max_order_quantity", UNSET)

        min_order_amount = d.pop("min_order_amount", UNSET)

        min_order_quantity = d.pop("min_order_quantity", UNSET)

        min_tick_size = d.pop("min_tick_size", UNSET)

        price_precision = d.pop("price_precision", UNSET)

        quantity_precision = d.pop("quantity_precision", UNSET)

        sell_enabled = d.pop("sell_enabled", UNSET)

        trader_market_details = cls(
            active=active,
            amount_precision=amount_precision,
            buy_enabled=buy_enabled,
            max_order_amount=max_order_amount,
            max_order_quantity=max_order_quantity,
            min_order_amount=min_order_amount,
            min_order_quantity=min_order_quantity,
            min_tick_size=min_tick_size,
            price_precision=price_precision,
            quantity_precision=quantity_precision,
            sell_enabled=sell_enabled,
        )

        trader_market_details.additional_properties = d
        return trader_market_details

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
