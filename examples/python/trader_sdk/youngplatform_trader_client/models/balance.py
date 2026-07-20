from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Balance")


@_attrs_define
class Balance:
    """
    Attributes:
        amount (str | Unset): Spendable amount in this vault.
        currency (str | Unset): Currency code the balance is denominated in. Example: BTC.
        vault_id (int | Unset): Numeric ID of the vault.
        vault_type (str | Unset): Vault type holding the balance (e.g. the spot wallet or a dedicated
            trading vault).
    """

    amount: str | Unset = UNSET
    currency: str | Unset = UNSET
    vault_id: int | Unset = UNSET
    vault_type: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        amount = self.amount

        currency = self.currency

        vault_id = self.vault_id

        vault_type = self.vault_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if amount is not UNSET:
            field_dict["amount"] = amount
        if currency is not UNSET:
            field_dict["currency"] = currency
        if vault_id is not UNSET:
            field_dict["vault_id"] = vault_id
        if vault_type is not UNSET:
            field_dict["vault_type"] = vault_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        amount = d.pop("amount", UNSET)

        currency = d.pop("currency", UNSET)

        vault_id = d.pop("vault_id", UNSET)

        vault_type = d.pop("vault_type", UNSET)

        balance = cls(
            amount=amount,
            currency=currency,
            vault_id=vault_id,
            vault_type=vault_type,
        )

        balance.additional_properties = d
        return balance

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
