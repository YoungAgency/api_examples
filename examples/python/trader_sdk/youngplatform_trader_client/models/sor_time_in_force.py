from enum import IntEnum


class SorTimeInForce(IntEnum):
    SOR_TIME_IN_FORCE_FOK = 1
    SOR_TIME_IN_FORCE_IOC = 2

    def __str__(self) -> str:
        return str(self.value)
