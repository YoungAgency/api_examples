from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.side import Side
from ..models.sor_order_status import SorOrderStatus
from ..models.sor_order_type import SorOrderType
from ..models.sor_time_in_force import SorTimeInForce
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.sor_order_match import SorOrderMatch


T = TypeVar("T", bound="SorOrder")


@_attrs_define
class SorOrder:
    """
    Attributes:
        amount (str | Unset): Requested amount (quantity x price), in quote currency.
        cid (int | Unset): Customer ID owning the order.
        client_order_id (str | Unset): Caller-supplied idempotency key (UUID); the stable reference for lookups.
        closed_at (str | Unset): Time the order reached a terminal status (null while still open).
        created_at (str | Unset): Time the order was accepted.
        fee (str | Unset): Fee charged on the order, in quote currency.
        ip (str | Unset): IP the order was placed from (not returned on the trader API).
        market (str | Unset): Market symbol in BASE-QUOTE format. Example: BTC-EUR.
        matched_amount (str | Unset): Amount filled so far, in quote currency.
        matched_quantity (str | Unset): Quantity filled so far, in base currency.
        matches (list[SorOrderMatch] | Unset): Individual fills; populated on order lookup and, when with_trades=true,
            on order history.
        order_id (int | Unset): Internal numeric order ID (0 in API responses; use client_order_id).
        price (str | Unset): Limit price, in quote currency.
        quantity (str | Unset): Requested quantity, in base currency.
        side (Side | Unset):
        status (SorOrderStatus | Unset):
        time_in_force (SorTimeInForce | Unset):
        type_ (SorOrderType | Unset):
        updated_at (str | Unset): Time of the last status change.
    """

    amount: str | Unset = UNSET
    cid: int | Unset = UNSET
    client_order_id: str | Unset = UNSET
    closed_at: str | Unset = UNSET
    created_at: str | Unset = UNSET
    fee: str | Unset = UNSET
    ip: str | Unset = UNSET
    market: str | Unset = UNSET
    matched_amount: str | Unset = UNSET
    matched_quantity: str | Unset = UNSET
    matches: list[SorOrderMatch] | Unset = UNSET
    order_id: int | Unset = UNSET
    price: str | Unset = UNSET
    quantity: str | Unset = UNSET
    side: Side | Unset = UNSET
    status: SorOrderStatus | Unset = UNSET
    time_in_force: SorTimeInForce | Unset = UNSET
    type_: SorOrderType | Unset = UNSET
    updated_at: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        amount = self.amount

        cid = self.cid

        client_order_id = self.client_order_id

        closed_at = self.closed_at

        created_at = self.created_at

        fee = self.fee

        ip = self.ip

        market = self.market

        matched_amount = self.matched_amount

        matched_quantity = self.matched_quantity

        matches: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.matches, Unset):
            matches = []
            for matches_item_data in self.matches:
                matches_item = matches_item_data.to_dict()
                matches.append(matches_item)

        order_id = self.order_id

        price = self.price

        quantity = self.quantity

        side: int | Unset = UNSET
        if not isinstance(self.side, Unset):
            side = self.side.value

        status: int | Unset = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        time_in_force: int | Unset = UNSET
        if not isinstance(self.time_in_force, Unset):
            time_in_force = self.time_in_force.value

        type_: int | Unset = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        updated_at = self.updated_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if amount is not UNSET:
            field_dict["amount"] = amount
        if cid is not UNSET:
            field_dict["cid"] = cid
        if client_order_id is not UNSET:
            field_dict["client_order_id"] = client_order_id
        if closed_at is not UNSET:
            field_dict["closed_at"] = closed_at
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if fee is not UNSET:
            field_dict["fee"] = fee
        if ip is not UNSET:
            field_dict["ip"] = ip
        if market is not UNSET:
            field_dict["market"] = market
        if matched_amount is not UNSET:
            field_dict["matched_amount"] = matched_amount
        if matched_quantity is not UNSET:
            field_dict["matched_quantity"] = matched_quantity
        if matches is not UNSET:
            field_dict["matches"] = matches
        if order_id is not UNSET:
            field_dict["order_id"] = order_id
        if price is not UNSET:
            field_dict["price"] = price
        if quantity is not UNSET:
            field_dict["quantity"] = quantity
        if side is not UNSET:
            field_dict["side"] = side
        if status is not UNSET:
            field_dict["status"] = status
        if time_in_force is not UNSET:
            field_dict["time_in_force"] = time_in_force
        if type_ is not UNSET:
            field_dict["type"] = type_
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.sor_order_match import SorOrderMatch

        d = dict(src_dict)
        amount = d.pop("amount", UNSET)

        cid = d.pop("cid", UNSET)

        client_order_id = d.pop("client_order_id", UNSET)

        closed_at = d.pop("closed_at", UNSET)

        created_at = d.pop("created_at", UNSET)

        fee = d.pop("fee", UNSET)

        ip = d.pop("ip", UNSET)

        market = d.pop("market", UNSET)

        matched_amount = d.pop("matched_amount", UNSET)

        matched_quantity = d.pop("matched_quantity", UNSET)

        _matches = d.pop("matches", UNSET)
        matches: list[SorOrderMatch] | Unset = UNSET
        if _matches is not UNSET:
            matches = []
            for matches_item_data in _matches:
                matches_item = SorOrderMatch.from_dict(matches_item_data)

                matches.append(matches_item)

        order_id = d.pop("order_id", UNSET)

        price = d.pop("price", UNSET)

        quantity = d.pop("quantity", UNSET)

        _side = d.pop("side", UNSET)
        side: Side | Unset
        if isinstance(_side, Unset):
            side = UNSET
        else:
            side = Side(_side)

        _status = d.pop("status", UNSET)
        status: SorOrderStatus | Unset
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = SorOrderStatus(_status)

        _time_in_force = d.pop("time_in_force", UNSET)
        time_in_force: SorTimeInForce | Unset
        if isinstance(_time_in_force, Unset):
            time_in_force = UNSET
        else:
            time_in_force = SorTimeInForce(_time_in_force)

        _type_ = d.pop("type", UNSET)
        type_: SorOrderType | Unset
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = SorOrderType(_type_)

        updated_at = d.pop("updated_at", UNSET)

        sor_order = cls(
            amount=amount,
            cid=cid,
            client_order_id=client_order_id,
            closed_at=closed_at,
            created_at=created_at,
            fee=fee,
            ip=ip,
            market=market,
            matched_amount=matched_amount,
            matched_quantity=matched_quantity,
            matches=matches,
            order_id=order_id,
            price=price,
            quantity=quantity,
            side=side,
            status=status,
            time_in_force=time_in_force,
            type_=type_,
            updated_at=updated_at,
        )

        sor_order.additional_properties = d
        return sor_order

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
