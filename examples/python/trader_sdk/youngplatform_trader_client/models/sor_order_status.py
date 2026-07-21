from enum import IntEnum


class SorOrderStatus(IntEnum):
    SOR_ORDER_STATUS_NEW = 1
    SOR_ORDER_STATUS_PARTIALLY_FILLED = 2
    SOR_ORDER_STATUS_FILLED = 3
    SOR_ORDER_STATUS_CANCELLED = 4
    SOR_ORDER_STATUS_EXPIRED = 5
    SOR_ORDER_STATUS_REJECTED = 6

    def __str__(self) -> str:
        return str(self.value)
