from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.cursor import Cursor
    from ..models.sor_order_match_item import SorOrderMatchItem


T = TypeVar("T", bound="SorMatchPage")


@_attrs_define
class SorMatchPage:
    """
    Attributes:
        data (list[SorOrderMatchItem] | Unset): Items on this page, most recent first.
        has_more (bool | Unset): Whether more items exist beyond this page.
        next_cursor (Cursor | Unset):
    """

    data: list[SorOrderMatchItem] | Unset = UNSET
    has_more: bool | Unset = UNSET
    next_cursor: Cursor | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.data, Unset):
            data = []
            for data_item_data in self.data:
                data_item = data_item_data.to_dict()
                data.append(data_item)

        has_more = self.has_more

        next_cursor: dict[str, Any] | Unset = UNSET
        if not isinstance(self.next_cursor, Unset):
            next_cursor = self.next_cursor.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if data is not UNSET:
            field_dict["data"] = data
        if has_more is not UNSET:
            field_dict["has_more"] = has_more
        if next_cursor is not UNSET:
            field_dict["next_cursor"] = next_cursor

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.cursor import Cursor
        from ..models.sor_order_match_item import SorOrderMatchItem

        d = dict(src_dict)
        _data = d.pop("data", UNSET)
        data: list[SorOrderMatchItem] | Unset = UNSET
        if _data is not UNSET:
            data = []
            for data_item_data in _data:
                data_item = SorOrderMatchItem.from_dict(data_item_data)

                data.append(data_item)

        has_more = d.pop("has_more", UNSET)

        _next_cursor = d.pop("next_cursor", UNSET)
        next_cursor: Cursor | Unset
        if isinstance(_next_cursor, Unset):
            next_cursor = UNSET
        else:
            next_cursor = Cursor.from_dict(_next_cursor)

        sor_match_page = cls(
            data=data,
            has_more=has_more,
            next_cursor=next_cursor,
        )

        sor_match_page.additional_properties = d
        return sor_match_page

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
