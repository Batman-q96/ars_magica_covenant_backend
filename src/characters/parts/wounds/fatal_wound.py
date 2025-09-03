from typing import ClassVar


import pydantic

from characters.parts.wounds import i_wound


class HealingDeathException(Exception):
    """Exception raised when someone tries to heal a fatal wound"""


class FatalWound(i_wound.IWound):
    """Fatal wounds mean the character is dead"""

    bonus: ClassVar[None] = None
    _STABLE_EASE_FACTOR: ClassVar[None] = None
    _RECOVERY_EASE_FACTOR: ClassVar[None] = None
    _STABLE_RECOVERY_BONUS: ClassVar[None] = None
    recovery_bonus: None = pydantic.Field(default=None, init_var=False, frozen=True)
    RECOVERY_PERIOD: None = pydantic.Field(default=None, init_var=False, frozen=True)

    def heal_based_on_recovery_result(self, recovery_result: int) -> None:
        """You can't heal a fatal wound normally"""
        raise HealingDeathException()
