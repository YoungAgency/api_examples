from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="FeeTier")


@_attrs_define
class FeeTier:
    """
    Attributes:
        fee_fixed (float | Unset): Fixed fee component of the tier.
        id (str | Unset): Tier identifier.
        max_volume_eur (float | Unset): Upper volume bound of the tier, in EUR (exclusive); null on the last
            (unbounded) tier.
        min_volume_eur (float | Unset): Lower volume bound of the tier, in EUR (inclusive).
        perc_fee_bps (int | Unset): Percentage fee of the tier, in basis points (1 bps = 0.01%).
    """

    fee_fixed: float | Unset = UNSET
    id: str | Unset = UNSET
    max_volume_eur: float | Unset = UNSET
    min_volume_eur: float | Unset = UNSET
    perc_fee_bps: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        fee_fixed = self.fee_fixed

        id = self.id

        max_volume_eur = self.max_volume_eur

        min_volume_eur = self.min_volume_eur

        perc_fee_bps = self.perc_fee_bps

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if fee_fixed is not UNSET:
            field_dict["fee_fixed"] = fee_fixed
        if id is not UNSET:
            field_dict["id"] = id
        if max_volume_eur is not UNSET:
            field_dict["max_volume_eur"] = max_volume_eur
        if min_volume_eur is not UNSET:
            field_dict["min_volume_eur"] = min_volume_eur
        if perc_fee_bps is not UNSET:
            field_dict["perc_fee_bps"] = perc_fee_bps

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        fee_fixed = d.pop("fee_fixed", UNSET)

        id = d.pop("id", UNSET)

        max_volume_eur = d.pop("max_volume_eur", UNSET)

        min_volume_eur = d.pop("min_volume_eur", UNSET)

        perc_fee_bps = d.pop("perc_fee_bps", UNSET)

        fee_tier = cls(
            fee_fixed=fee_fixed,
            id=id,
            max_volume_eur=max_volume_eur,
            min_volume_eur=min_volume_eur,
            perc_fee_bps=perc_fee_bps,
        )

        fee_tier.additional_properties = d
        return fee_tier

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
