"""Generic character"""

from typing import Optional, Any
import datetime

from dateutil import relativedelta
import pydantic

from characters.parts import (
    wound_tracker as parts_wounds,
)

from characters.types import i_character


def _get_deltas_in_larger_relative_delta(
    *,
    short_duration: Optional[relativedelta.relativedelta] = None,
    long_duration: relativedelta.relativedelta,
    start_date: Optional[datetime.datetime] = None,
) -> int:
    """Helper function to get the number of weeks in a relative delta because we
    can't easily convert between months and weeks"""
    short_duration = (
        relativedelta.relativedelta(weeks=1)
        if short_duration is None
        else short_duration
    )
    start_date = datetime.datetime.today() if start_date is None else start_date
    end_date = start_date + long_duration
    counter = -1  # this way we roudn down to the nearest full number of weeks
    while end_date > start_date:
        counter += 1
        end_date -= short_duration
    return counter


class BaseCharacter(i_character.ICharacter):
    """Base character class"""

    _wound_tracker: parts_wounds.WoundTracker = pydantic.PrivateAttr()

    def model_post_init(self, __context: Any) -> None:
        """Initialze base char as needed"""
        self._wound_tracker = parts_wounds.WoundTracker(size=self.size)

    def take_damage(self, damage: int) -> None:
        """Take a hit and add an appopriate wound"""
        self._wound_tracker.take_damage(damage)

    def recover(
        self, duration: relativedelta.relativedelta, recovery_roll: Optional[int] = None
    ) -> None:
        """Recover all wounds of the appropriate time duration"""


b = BaseCharacter(
    traits=[],
    abilities=[],
    flaws=[],
    virtues=[],
    reputations=[],
)
print(b)
