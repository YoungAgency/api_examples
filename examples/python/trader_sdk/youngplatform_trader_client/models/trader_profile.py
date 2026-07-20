from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.fee_tier import FeeTier
    from ..models.profile_tier import ProfileTier


T = TypeVar("T", bound="TraderProfile")


@_attrs_define
class TraderProfile:
    """
    Attributes:
        cid (int | Unset): Customer ID the profile belongs to.
        rolling_volume_eur (float | Unset): RollingVolumeEur is the customer's trailing 30-day EUR volume, refreshed
            once a day at 05:00 UTC. The tier/volume axis is float64-native in the
            domain (see FeeTier.MinVolumeEur), so it is kept as float64.
        sor_discount_percentage (str | Unset): SorDiscountPercentage is the discount currently applied to SOR orders at
            the customer's rolling volume: the club discount below the volume cap, the
            non-club (fee-user-group) discount once the volume exceeds the cap.
        sor_tier (ProfileTier | Unset):
        sor_tiers (list[FeeTier] | Unset): SorTiers is the full SOR fee tier ladder (volume bands and fees), so a
            caller can see all thresholds — e.g. how much volume separates the
            customer from the next tier. The ladder is identical across markets.
    """

    cid: int | Unset = UNSET
    rolling_volume_eur: float | Unset = UNSET
    sor_discount_percentage: str | Unset = UNSET
    sor_tier: ProfileTier | Unset = UNSET
    sor_tiers: list[FeeTier] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        cid = self.cid

        rolling_volume_eur = self.rolling_volume_eur

        sor_discount_percentage = self.sor_discount_percentage

        sor_tier: dict[str, Any] | Unset = UNSET
        if not isinstance(self.sor_tier, Unset):
            sor_tier = self.sor_tier.to_dict()

        sor_tiers: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.sor_tiers, Unset):
            sor_tiers = []
            for sor_tiers_item_data in self.sor_tiers:
                sor_tiers_item = sor_tiers_item_data.to_dict()
                sor_tiers.append(sor_tiers_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if cid is not UNSET:
            field_dict["cid"] = cid
        if rolling_volume_eur is not UNSET:
            field_dict["rolling_volume_eur"] = rolling_volume_eur
        if sor_discount_percentage is not UNSET:
            field_dict["sor_discount_percentage"] = sor_discount_percentage
        if sor_tier is not UNSET:
            field_dict["sor_tier"] = sor_tier
        if sor_tiers is not UNSET:
            field_dict["sor_tiers"] = sor_tiers

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.fee_tier import FeeTier
        from ..models.profile_tier import ProfileTier

        d = dict(src_dict)
        cid = d.pop("cid", UNSET)

        rolling_volume_eur = d.pop("rolling_volume_eur", UNSET)

        sor_discount_percentage = d.pop("sor_discount_percentage", UNSET)

        _sor_tier = d.pop("sor_tier", UNSET)
        sor_tier: ProfileTier | Unset
        if isinstance(_sor_tier, Unset):
            sor_tier = UNSET
        else:
            sor_tier = ProfileTier.from_dict(_sor_tier)

        _sor_tiers = d.pop("sor_tiers", UNSET)
        sor_tiers: list[FeeTier] | Unset = UNSET
        if _sor_tiers is not UNSET:
            sor_tiers = []
            for sor_tiers_item_data in _sor_tiers:
                sor_tiers_item = FeeTier.from_dict(sor_tiers_item_data)

                sor_tiers.append(sor_tiers_item)

        trader_profile = cls(
            cid=cid,
            rolling_volume_eur=rolling_volume_eur,
            sor_discount_percentage=sor_discount_percentage,
            sor_tier=sor_tier,
            sor_tiers=sor_tiers,
        )

        trader_profile.additional_properties = d
        return trader_profile

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
