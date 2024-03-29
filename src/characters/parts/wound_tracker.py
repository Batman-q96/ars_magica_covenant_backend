"""Wounding is the consequence of damage Arm5(178-180)"""

from typing import Optional, Callable, Sequence, ClassVar
import math
import enum
import datetime
import abc
from dateutil import relativedelta

import pydantic

from lib import am5_rolls


class WoundStatus(enum.Enum):
    """Enum to determine result of healing roll"""

    WORSE = -1
    SAME = 0
    BETTER = 1


class Wound(pydantic.BaseModel, abc.ABC):
    """Basic wound"""

    model_config = pydantic.ConfigDict(
        validate_assignment=True, arbitrary_types_allowed=True
    )
    bonus: int | None
    status: WoundStatus = WoundStatus.SAME
    _STABLE_EASE_FACTOR: ClassVar[Optional[int]]
    _RECOVERY_EASE_FACTOR: ClassVar[Optional[int]]
    _STABLE_RECOVERY_BONUS: ClassVar[Optional[int]]
    recovery_bonus: int | None = pydantic.Field(default=0, ge=0, multiple_of=3)
    recovery_period: relativedelta.relativedelta | None

    @abc.abstractmethod
    def heal(self, recovery_result: int) -> None:
        """Basic function to heal a wound"""
        raise NotImplementedError


class _StandardWound(Wound):
    """Standard wounds are light, medium, heavy, and incapacitating"""

    bonus: int
    _STABLE_EASE_FACTOR: ClassVar[int]
    _RECOVERY_EASE_FACTOR: ClassVar[int]
    _STABLE_RECOVERY_BONUS: ClassVar[int] = 3
    recovery_bonus: int = pydantic.Field(default=0, ge=0, multiple_of=3)
    recovery_period: relativedelta.relativedelta

    def heal(self, recovery_result: int) -> None:
        """Healing for these wounds depends on their ease factors"""
        if recovery_result < self._STABLE_EASE_FACTOR:
            self.status = WoundStatus.WORSE
        elif (
            self._STABLE_EASE_FACTOR <= recovery_result
            and recovery_result < self._RECOVERY_EASE_FACTOR
        ):
            self.status = WoundStatus.SAME
            self.recovery_bonus += self._STABLE_RECOVERY_BONUS
        elif self._RECOVERY_EASE_FACTOR <= recovery_result:
            self.status = WoundStatus.BETTER


class LightWound(_StandardWound):
    """Light wounds are easiest to heal"""

    bonus: ClassVar[int] = -1
    _STABLE_EASE_FACTOR: ClassVar[int] = 4
    _RECOVERY_EASE_FACTOR: ClassVar[int] = 10
    _STABLE_RECOVERY_BONUS: ClassVar[int] = 3
    recovery_period: datetime.timedelta = pydantic.Field(
        default=relativedelta.relativedelta(weeks=1), init_var=False, frozen=True
    )


class MediumWound(_StandardWound):
    """Medium wounds are more serious than light ones"""

    bonus: ClassVar[int] = -3
    _STABLE_EASE_FACTOR: ClassVar[int] = 6
    _RECOVERY_EASE_FACTOR: ClassVar[int] = 12
    _STABLE_RECOVERY_BONUS: ClassVar[int] = 3
    recovery_period: datetime.timedelta = pydantic.Field(
        default=relativedelta.relativedelta(months=1), init_var=False, frozen=True
    )


class HeavyWound(_StandardWound):
    """Heavy wounds are the most serious typical wounds"""

    bonus: ClassVar[int] = -5
    _STABLE_EASE_FACTOR: ClassVar[int] = 9
    _RECOVERY_EASE_FACTOR: ClassVar[int] = 15
    _STABLE_RECOVERY_BONUS: ClassVar[int] = 3
    recovery_period: datetime.timedelta = pydantic.Field(
        default=relativedelta.relativedelta(months=3), init_var=False, frozen=True
    )


class IncapacitatingWound(_StandardWound):
    """Incapacitating wounds will prevent a character from enagaging in any serious activity"""

    bonus: ClassVar[None] = None
    _STABLE_EASE_FACTOR: ClassVar[int] = 0
    _RECOVERY_EASE_FACTOR: ClassVar[int] = 9
    _STABLE_RECOVERY_BONUS: ClassVar[int] = -1
    recovery_period: datetime.timedelta = pydantic.Field(
        default=relativedelta.relativedelta(hours=12), init_var=False, frozen=True
    )
    recovery_bonus: int = pydantic.Field(default=0, le=0)


class FatalWound(Wound):
    """Fatal wounds mean the character is dead"""

    bonus: ClassVar[None] = None
    _STABLE_EASE_FACTOR: ClassVar[None] = None
    _RECOVERY_EASE_FACTOR: ClassVar[None] = None
    _STABLE_RECOVERY_BONUS: ClassVar[None] = None
    recovery_bonus: None = pydantic.Field(default=None, init_var=False, frozen=True)
    recovery_period: None = pydantic.Field(default=None, init_var=False, frozen=True)

    def heal(self, recovery_result: int) -> None:
        """You can't heal a fatal wound normally"""
        raise HealingDeathException()


class HealingDeathException(Exception):
    """Exception raised when someone tries to heal a fatal wound"""


class WoundTracker(pydantic.BaseModel):
    """Class to track wounds on a character"""

    _modified_size: int
    _light_wounds: list[LightWound] = []
    _medium_wounds: list[MediumWound] = []
    _heavy_wounds: list[HeavyWound] = []
    _incapacitating_wound: Optional[IncapacitatingWound] = None
    _fatal_wound: Optional[FatalWound] = None

    def __init__(self, size: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # size is shifted up by 5 for easier math elsewhere
        # see below table from ArM5 179
        # Size          Light   Medium  Heavy   Incapacitating  Dead
        # –4 or less    1       2       3       4               5+
        # –3            1–2     3–4     5–6     7–8             9+
        # –2            1–3     4–6     7–9     10–12           13+
        # –1            1–4     5–8     9–12    13–16           17+
        # 0             1–5     6–10    11–15   16–20           21+
        self._modified_size = size + 5

    @pydantic.computed_field
    @property
    def wound_bonus(self) -> int | None:
        """Determine what the penalty to activities is based on wound state"""
        if self.dead or self.incapacitated:
            return None
        else:
            return sum(
                [
                    wound.bonus
                    for wound in self._light_wounds
                    + self._medium_wounds
                    + self._heavy_wounds
                ]
            )

    @pydantic.computed_field
    @property
    def light_wounds(self) -> int:
        """Number of light wounds that this character has"""
        return len(self._light_wounds)

    @pydantic.computed_field
    @property
    def medium_wounds(self) -> int:
        """Number of medium wounds that this character has"""
        return len(self._medium_wounds)

    @pydantic.computed_field
    @property
    def heavy_wounds(self) -> int:
        """Number of heavy wounds that this character has"""
        return len(self._heavy_wounds)

    @pydantic.computed_field
    @property
    def incapacitated(self) -> bool:
        """Determine if this character is incapacitated due to wounds"""
        if self._incapacitating_wound:
            return True
        else:
            return False

    @pydantic.computed_field
    @property
    def dead(self) -> bool:
        """Determine if this character is dead due to wounds"""
        if self._fatal_wound:
            return True
        else:
            return False

    # helper functions to add generic wound of a specific type
    def _add_light_wound(self) -> LightWound:
        wound = LightWound()
        self._light_wounds.append(wound)
        return wound

    def _add_medium_wound(self) -> MediumWound:
        wound = MediumWound()
        self._medium_wounds.append(wound)
        return wound

    def _add_heavy_wound(self) -> HeavyWound:
        wound = HeavyWound()
        self._heavy_wounds.append(wound)
        return wound

    def _add_incapacitating_wound(self) -> IncapacitatingWound:
        wound = IncapacitatingWound()
        self._incapacitating_wound = wound
        return wound

    def _add_fatal_wound(self) -> FatalWound:
        wound = FatalWound()
        self._fatal_wound = wound
        return wound

    def add_wound(self, wound: Wound) -> None:
        """Add a wound of a particular type"""
        if isinstance(wound, LightWound):
            self._light_wounds.append(wound)
        elif isinstance(wound, MediumWound):
            self._medium_wounds.append(wound)
        elif isinstance(wound, HeavyWound):
            self._heavy_wounds.append(wound)
        elif isinstance(wound, IncapacitatingWound):
            self._incapacitating_wound = wound
        elif isinstance(wound, FatalWound):
            self._fatal_wound = wound
        else:
            raise TypeError

    def take_damage(self, damage: int) -> Wound:
        """Take some amount of damage and add a wound of that type"""
        wound_level = math.ceil(damage / self._modified_size)
        if 1 == wound_level:
            return self._add_light_wound()
        elif 2 == wound_level:
            return self._add_medium_wound()
        elif 3 == wound_level:
            return self._add_heavy_wound()
        elif 4 == wound_level:
            return self._add_incapacitating_wound()
        elif 5 <= wound_level:
            return self._add_fatal_wound()
        else:
            raise ValueError

    def _recover_all_wounds_of_one_type(
        self,
        wound_list: Sequence[Wound],
        wound_got_better_function: Callable,
        wound_got_worse_function: Callable,
        recovery_bonus: int,
        recovery_roll_results: Optional[int | Sequence[Optional[int]]] = None,
    ) -> Sequence[Wound]:
        if recovery_roll_results is None:
            recovery_roll_results = [None] * len(wound_list)
        elif isinstance(recovery_roll_results, int):
            recovery_roll_results = [recovery_roll_results] * len(wound_list)
        for wound, roll_result in zip(wound_list, recovery_roll_results):
            try:
                if roll_result is None:
                    roll_result = am5_rolls.roll_stress()
                wound.heal(roll_result + recovery_bonus)
                if wound.status == WoundStatus.BETTER:
                    wound_got_better_function()
                elif wound.status == WoundStatus.WORSE:
                    wound_got_worse_function()
            except am5_rolls.BotchedRollExcption:
                wound.status = WoundStatus.WORSE
                wound_got_worse_function()
        return [wound for wound in wound_list if wound.status == WoundStatus.SAME]

    def recover_all_light_wounds(
        self,
        recovery_bonus: int,
        recovery_roll_results: Optional[int | Sequence[Optional[int]]] = None,
    ):
        """Make recovery rolls (and follow through on results) for all light wounds"""
        remaining_light_wounds = self._recover_all_wounds_of_one_type(
            self._light_wounds,
            lambda: (),
            self._add_medium_wound,
            recovery_bonus,
            recovery_roll_results,
        )
        # this filtration is not necessary if everythign works right, but
        # if we don't do it the type checker will complain
        self._light_wounds = [
            wound for wound in remaining_light_wounds if isinstance(wound, LightWound)
        ]

    def recover_all_medium_wounds(
        self,
        recovery_bonus: int,
        recovery_roll_results: Optional[int | Sequence[Optional[int]]] = None,
    ):
        """Make recovery rolls (and follow through on results) for all medium wounds"""
        remaining_medium_wounds = self._recover_all_wounds_of_one_type(
            self._medium_wounds,
            self._add_light_wound,
            self._add_heavy_wound,
            recovery_bonus,
            recovery_roll_results,
        )
        self._medium_wounds = [
            wound for wound in remaining_medium_wounds if isinstance(wound, MediumWound)
        ]

    def recover_all_heavy_wounds(
        self,
        recovery_bonus: int,
        recovery_roll_results: Optional[int | Sequence[Optional[int]]] = None,
    ):
        """Make recovery rolls (and follow through on results) for all heavy wounds"""
        remaining_heavy_wounds = self._recover_all_wounds_of_one_type(
            self._heavy_wounds,
            self._add_medium_wound,
            self._add_incapacitating_wound,
            recovery_bonus,
            recovery_roll_results,
        )
        self._heavy_wounds = [
            wound for wound in remaining_heavy_wounds if isinstance(wound, HeavyWound)
        ]

    def recover_all_incapacitating_wounds(
        self,
        recovery_bonus: int,
        recovery_roll_results: Optional[int | Sequence[Optional[int]]] = None,
    ):
        """Make recovery rolls (and follow through on results) for incapacitating wounds"""
        if self._incapacitating_wound is None:
            return

        returned_wounds = self._recover_all_wounds_of_one_type(
            [self._incapacitating_wound],
            self._add_heavy_wound,
            self._add_fatal_wound,
            recovery_bonus,
            recovery_roll_results,
        )
        remaining_incapacitating_wounds = [
            wound for wound in returned_wounds if isinstance(wound, IncapacitatingWound)
        ]
        if remaining_incapacitating_wounds:  # wound didn't get better or worse
            self._incapacitating_wound = remaining_incapacitating_wounds[0]
        else:  # wound got worse or better and thus we have no more incapacitating wound
            self._incapacitating_wound = None
