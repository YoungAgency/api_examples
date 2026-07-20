from enum import IntEnum


class SorOrderType(IntEnum):
    SOR_ORDER_TYPE_LIMIT = 1

    def __str__(self) -> str:
        return str(self.value)
