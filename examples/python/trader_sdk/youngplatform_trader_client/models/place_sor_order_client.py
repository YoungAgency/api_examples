from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.side import Side
from ..models.sor_order_type import SorOrderType
from ..models.sor_time_in_force import SorTimeInForce
from ..types import UNSET, Unset

T = TypeVar("T", bound="PlaceSorOrderClient")


@_attrs_define
class PlaceSorOrderClient:
    """
    Attributes:
        market (str): Market symbol in BASE-QUOTE format. Example: BTC-EUR.
        price (str): Limit price, in quote currency (decimal string).
        quantity (str): Quantity to trade, in base currency (decimal string).
        time_in_force (SorTimeInForce):
        type_ (SorOrderType):
        client_order_id (str | Unset): ClientOrderId is the caller-supplied idempotency key (a UUID) — required on
            the trader HTTP API (the internal path generates one when empty). Retrying
            with the same value never places a second order, and the order can be
            reconciled after a timeout via GetOrder. Validated as a UUID service-side.
        side (Side | Unset):
    """

    market: str
    price: str
    quantity: str
    time_in_force: SorTimeInForce
    type_: SorOrderType
    client_order_id: str | Unset = UNSET
    side: Side | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        market = self.market

        price = self.price

        quantity = self.quantity

        time_in_force = self.time_in_force.value

        type_ = self.type_.value

        client_order_id = self.client_order_id

        side: int | Unset = UNSET
        if not isinstance(self.side, Unset):
            side = self.side.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "market": market,
                "price": price,
                "quantity": quantity,
                "time_in_force": time_in_force,
                "type": type_,
            }
        )
        if client_order_id is not UNSET:
            field_dict["client_order_id"] = client_order_id
        if side is not UNSET:
            field_dict["side"] = side

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        market = d.pop("market")

        price = d.pop("price")

        quantity = d.pop("quantity")

        time_in_force = SorTimeInForce(d.pop("time_in_force"))

        type_ = SorOrderType(d.pop("type"))

        client_order_id = d.pop("client_order_id", UNSET)

        _side = d.pop("side", UNSET)
        side: Side | Unset
        if isinstance(_side, Unset):
            side = UNSET
        else:
            side = Side(_side)

        place_sor_order_client = cls(
            market=market,
            price=price,
            quantity=quantity,
            time_in_force=time_in_force,
            type_=type_,
            client_order_id=client_order_id,
            side=side,
        )

        place_sor_order_client.additional_properties = d
        return place_sor_order_client

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
