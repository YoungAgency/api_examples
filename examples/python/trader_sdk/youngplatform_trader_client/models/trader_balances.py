from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.balance import Balance


T = TypeVar("T", bound="TraderBalances")


@_attrs_define
class TraderBalances:
    """
    Attributes:
        balances (list[Balance] | Unset): Per-vault balances of the authenticated customer.
    """

    balances: list[Balance] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        balances: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.balances, Unset):
            balances = []
            for balances_item_data in self.balances:
                balances_item = balances_item_data.to_dict()
                balances.append(balances_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if balances is not UNSET:
            field_dict["balances"] = balances

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.balance import Balance

        d = dict(src_dict)
        _balances = d.pop("balances", UNSET)
        balances: list[Balance] | Unset = UNSET
        if _balances is not UNSET:
            balances = []
            for balances_item_data in _balances:
                balances_item = Balance.from_dict(balances_item_data)

                balances.append(balances_item)

        trader_balances = cls(
            balances=balances,
        )

        trader_balances.additional_properties = d
        return trader_balances

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
