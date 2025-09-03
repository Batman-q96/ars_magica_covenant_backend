from typing import ClassVar, Optional
import abc

import pydantic
from dateutil import relativedelta

from characters.parts.wounds import wound_status


class IWound(pydantic.BaseModel, abc.ABC):
    """Wound Interface"""

    model_config = pydantic.ConfigDict(
        validate_assignment=True, arbitrary_types_allowed=True
    )
    bonus: int | None
    status: wound_status.WoundStatus = wound_status.WoundStatus.SAME
    _STABLE_EASE_FACTOR: ClassVar[Optional[int]]
    _RECOVERY_EASE_FACTOR: ClassVar[Optional[int]]
    _STABLE_RECOVERY_BONUS: ClassVar[Optional[int]]
    recovery_bonus: int | None = pydantic.Field(default=0, ge=0, multiple_of=3)
    RECOVERY_PERIOD: ClassVar[Optional[relativedelta.relativedelta]]

    @abc.abstractmethod
    def heal_based_on_recovery_result(self, recovery_result: int) -> None:
        """Basic function to heal a wound"""
        raise NotImplementedError
