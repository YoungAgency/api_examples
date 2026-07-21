from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SorOrderMatch")


@_attrs_define
class SorOrderMatch:
    """
    Attributes:
        amount (str | Unset): Filled amount (quantity x price), in quote currency.
        created_at (str | Unset): Time of the fill.
        fee (str | Unset): Venue fee for this fill, in fee_currency.
        fee_currency (str | Unset): Currency the venue fee is denominated in.
        id (int | Unset): Internal numeric match ID.
        price (str | Unset): Fill price, in quote currency.
        quantity (str | Unset): Filled quantity, in base currency.
        sor_order_id (int | Unset): Internal numeric ID of the parent SOR order.
        venue (str | Unset): Execution venue that filled this portion of the order.
        venue_match_id (str | Unset): Fill ID assigned by the venue.
        venue_order_id (str | Unset): Order ID assigned by the venue.
    """

    amount: str | Unset = UNSET
    created_at: str | Unset = UNSET
    fee: str | Unset = UNSET
    fee_currency: str | Unset = UNSET
    id: int | Unset = UNSET
    price: str | Unset = UNSET
    quantity: str | Unset = UNSET
    sor_order_id: int | Unset = UNSET
    venue: str | Unset = UNSET
    venue_match_id: str | Unset = UNSET
    venue_order_id: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        amount = self.amount

        created_at = self.created_at

        fee = self.fee

        fee_currency = self.fee_currency

        id = self.id

        price = self.price

        quantity = self.quantity

        sor_order_id = self.sor_order_id

        venue = self.venue

        venue_match_id = self.venue_match_id

        venue_order_id = self.venue_order_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if amount is not UNSET:
            field_dict["amount"] = amount
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if fee is not UNSET:
            field_dict["fee"] = fee
        if fee_currency is not UNSET:
            field_dict["fee_currency"] = fee_currency
        if id is not UNSET:
            field_dict["id"] = id
        if price is not UNSET:
            field_dict["price"] = price
        if quantity is not UNSET:
            field_dict["quantity"] = quantity
        if sor_order_id is not UNSET:
            field_dict["sor_order_id"] = sor_order_id
        if venue is not UNSET:
            field_dict["venue"] = venue
        if venue_match_id is not UNSET:
            field_dict["venue_match_id"] = venue_match_id
        if venue_order_id is not UNSET:
            field_dict["venue_order_id"] = venue_order_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        amount = d.pop("amount", UNSET)

        created_at = d.pop("created_at", UNSET)

        fee = d.pop("fee", UNSET)

        fee_currency = d.pop("fee_currency", UNSET)

        id = d.pop("id", UNSET)

        price = d.pop("price", UNSET)

        quantity = d.pop("quantity", UNSET)

        sor_order_id = d.pop("sor_order_id", UNSET)

        venue = d.pop("venue", UNSET)

        venue_match_id = d.pop("venue_match_id", UNSET)

        venue_order_id = d.pop("venue_order_id", UNSET)

        sor_order_match = cls(
            amount=amount,
            created_at=created_at,
            fee=fee,
            fee_currency=fee_currency,
            id=id,
            price=price,
            quantity=quantity,
            sor_order_id=sor_order_id,
            venue=venue,
            venue_match_id=venue_match_id,
            venue_order_id=venue_order_id,
        )

        sor_order_match.additional_properties = d
        return sor_order_match

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
