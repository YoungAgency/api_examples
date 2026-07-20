from enum import IntEnum


class Side(IntEnum):
    SIDE_BUY = 1
    SIDE_SELL = 2

    def __str__(self) -> str:
        return str(self.value)
