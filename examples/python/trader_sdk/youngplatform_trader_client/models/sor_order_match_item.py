from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.side import Side
from ..types import UNSET, Unset

T = TypeVar("T", bound="SorOrderMatchItem")


@_attrs_define
class SorOrderMatchItem:
    """
    Attributes:
        amount (str | Unset): Filled amount (quantity x price), in quote currency.
        client_order_id (str | Unset): Client order id of the parent SOR order this fill belongs to.
        created_at (str | Unset): Time of the fill.
        fee (str | Unset): Venue fee for this fill, in fee_currency.
        fee_currency (str | Unset): Currency the venue fee is denominated in.
        id (int | Unset): Match id; pass it as before_id (with created_at as before) to resume
            keyset pagination from this fill. Matches NextCursor.ID.
        market (str | Unset): Market symbol in BASE-QUOTE format. Example: BTC-EUR.
        price (str | Unset): Fill price, in quote currency.
        quantity (str | Unset): Filled quantity, in base currency.
        side (Side | Unset):
        venue (str | Unset): Execution venue that filled this portion of the order.
        venue_match_id (str | Unset): Fill id assigned by the venue.
        venue_order_id (str | Unset): Order id assigned by the venue.
    """

    amount: str | Unset = UNSET
    client_order_id: str | Unset = UNSET
    created_at: str | Unset = UNSET
    fee: str | Unset = UNSET
    fee_currency: str | Unset = UNSET
    id: int | Unset = UNSET
    market: str | Unset = UNSET
    price: str | Unset = UNSET
    quantity: str | Unset = UNSET
    side: Side | Unset = UNSET
    venue: str | Unset = UNSET
    venue_match_id: str | Unset = UNSET
    venue_order_id: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        amount = self.amount

        client_order_id = self.client_order_id

        created_at = self.created_at

        fee = self.fee

        fee_currency = self.fee_currency

        id = self.id

        market = self.market

        price = self.price

        quantity = self.quantity

        side: int | Unset = UNSET
        if not isinstance(self.side, Unset):
            side = self.side.value

        venue = self.venue

        venue_match_id = self.venue_match_id

        venue_order_id = self.venue_order_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if amount is not UNSET:
            field_dict["amount"] = amount
        if client_order_id is not UNSET:
            field_dict["client_order_id"] = client_order_id
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if fee is not UNSET:
            field_dict["fee"] = fee
        if fee_currency is not UNSET:
            field_dict["fee_currency"] = fee_currency
        if id is not UNSET:
            field_dict["id"] = id
        if market is not UNSET:
            field_dict["market"] = market
        if price is not UNSET:
            field_dict["price"] = price
        if quantity is not UNSET:
            field_dict["quantity"] = quantity
        if side is not UNSET:
            field_dict["side"] = side
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

        client_order_id = d.pop("client_order_id", UNSET)

        created_at = d.pop("created_at", UNSET)

        fee = d.pop("fee", UNSET)

        fee_currency = d.pop("fee_currency", UNSET)

        id = d.pop("id", UNSET)

        market = d.pop("market", UNSET)

        price = d.pop("price", UNSET)

        quantity = d.pop("quantity", UNSET)

        _side = d.pop("side", UNSET)
        side: Side | Unset
        if isinstance(_side, Unset):
            side = UNSET
        else:
            side = Side(_side)

        venue = d.pop("venue", UNSET)

        venue_match_id = d.pop("venue_match_id", UNSET)

        venue_order_id = d.pop("venue_order_id", UNSET)

        sor_order_match_item = cls(
            amount=amount,
            client_order_id=client_order_id,
            created_at=created_at,
            fee=fee,
            fee_currency=fee_currency,
            id=id,
            market=market,
            price=price,
            quantity=quantity,
            side=side,
            venue=venue,
            venue_match_id=venue_match_id,
            venue_order_id=venue_order_id,
        )

        sor_order_match_item.additional_properties = d
        return sor_order_match_item

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
