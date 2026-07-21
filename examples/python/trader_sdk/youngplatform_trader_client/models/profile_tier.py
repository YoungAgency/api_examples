from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.fee_tier import FeeTier


T = TypeVar("T", bound="ProfileTier")


@_attrs_define
class ProfileTier:
    """
    Attributes:
        effective_fee_bps (int | Unset): EffectiveFeeBps is the tier's fee bps after applying SorDiscountPercentage.
        tier (FeeTier | Unset):
    """

    effective_fee_bps: int | Unset = UNSET
    tier: FeeTier | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        effective_fee_bps = self.effective_fee_bps

        tier: dict[str, Any] | Unset = UNSET
        if not isinstance(self.tier, Unset):
            tier = self.tier.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if effective_fee_bps is not UNSET:
            field_dict["effective_fee_bps"] = effective_fee_bps
        if tier is not UNSET:
            field_dict["tier"] = tier

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.fee_tier import FeeTier

        d = dict(src_dict)
        effective_fee_bps = d.pop("effective_fee_bps", UNSET)

        _tier = d.pop("tier", UNSET)
        tier: FeeTier | Unset
        if isinstance(_tier, Unset):
            tier = UNSET
        else:
            tier = FeeTier.from_dict(_tier)

        profile_tier = cls(
            effective_fee_bps=effective_fee_bps,
            tier=tier,
        )

        profile_tier.additional_properties = d
        return profile_tier

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
