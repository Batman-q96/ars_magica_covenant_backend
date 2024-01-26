from typing import Optional, Callable, Sequence
import math
import enum
import datetime
from dateutil import relativedelta

import pydantic

from lib import am5_rolls

class WoundStatus(enum.Enum):
    WORSE = -1
    SAME = 0
    BETTER = 1

class Wound(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(validate_assignment=True, arbitrary_types_allowed=True)
    bonus: int | None
    status: WoundStatus = WoundStatus.SAME
    recovery_bonus: int | None = pydantic.Field(default=0, ge=0, multiple_of=3)
    recovery_period: relativedelta.relativedelta | None
class LightWound(Wound):
    bonus: int = pydantic.Field(default=-1, init_var=False, frozen=True)
    recovery_period: datetime.timedelta = pydantic.Field(default=relativedelta.relativedelta(weeks=1), init_var=False, frozen=True)
class MediumWound(Wound):
    bonus: int = pydantic.Field(default=-3, init_var=False, frozen=True)
    recovery_period: datetime.timedelta = pydantic.Field(default=relativedelta.relativedelta(months=1), init_var=False, frozen=True)
class HeavyWound(Wound):
    bonus: int = pydantic.Field(default=-5, init_var=False, frozen=True)
    recovery_period: datetime.timedelta = pydantic.Field(default=relativedelta.relativedelta(months=3), init_var=False, frozen=True)
class IncapacitatingWound(Wound):
    bonus: None = pydantic.Field(default=None, init_var=False, frozen=True)
    recovery_period: datetime.timedelta = pydantic.Field(default=relativedelta.relativedelta(hours=12), init_var=False, frozen=True)
    recovery_bonus: int = pydantic.Field(default=0, le=0)
class DeadlyWound(Wound):
    bonus: None = pydantic.Field(default=None, init_var=False, frozen=True)
    recovery_bonus: None = pydantic.Field(default=None, init_var=False, frozen=True)
    recovery_period: None = pydantic.Field(default=None, init_var=False, frozen=True)

class WoundTracker(pydantic.BaseModel):
    _modified_size: int
    _light_wounds: list[LightWound] = []
    _medium_wounds: list[MediumWound] = []
    _heavy_wounds: list[HeavyWound] = []
    _incapacitating_wound: Optional[IncapacitatingWound] = None
    _deadly_wound: Optional[DeadlyWound] = None

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
        self._modified_size = size+5

    @pydantic.computed_field
    @property
    def wound_bonus(self) -> int | None:
        if self.dead or self.incapacitated:
            return None
        else:
            return sum([wound.bonus for wound in self._light_wounds+self._medium_wounds+self._heavy_wounds])
    
    @pydantic.computed_field
    @property
    def incapacitated(self) -> bool:
        if self._incapacitating_wound:
            return True
        else:
            return False
    
    @pydantic.computed_field
    @property
    def dead(self) -> bool:
        if self._deadly_wound:
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
    def _add_deadly_wound(self) -> DeadlyWound:
        wound = DeadlyWound()
        self._deadly_wound = wound
        return wound
    
    def add_wound(self, wound: Wound) -> None:
        if isinstance(wound, LightWound):
            self._light_wounds.append(wound)
        elif isinstance(wound, MediumWound):
            self._medium_wounds.append(wound)
        elif isinstance(wound, HeavyWound):
            self._heavy_wounds.append(wound)
        elif isinstance(wound, IncapacitatingWound):
            self._incapacitating_wound = wound
        elif isinstance(wound, DeadlyWound):
            self._deadly_wound = wound
        else:
            raise TypeError

    def take_damage(self, damage) -> Wound:
        wound_level = math.ceil(damage/self._modified_size)
        if 1 == wound_level:
            return self._add_light_wound()
        elif 2 == wound_level:
            return self._add_medium_wound()
        elif 3 == wound_level:
            return self._add_heavy_wound()
        elif 4 == wound_level:
            return self._add_incapacitating_wound()
        elif 5 <= wound_level:
            return self._add_deadly_wound()
        else:
            raise ValueError
    
    def _recover_wound(self,
            wound: Wound,
            recovery_result: int,
            stable_ease_factor: int,
            improvement_ease_factor: int,
            wound_recovery_bonus: int
        ) -> None:
        if not wound.recovery_bonus:
            return
        if recovery_result < stable_ease_factor:
            wound.status = WoundStatus.BETTER
        elif stable_ease_factor <= recovery_result and recovery_result < improvement_ease_factor:
            wound.status = WoundStatus.SAME
            wound.recovery_bonus += wound_recovery_bonus
        elif improvement_ease_factor <= recovery_result:
            wound.status = WoundStatus.BETTER
        else:
            raise ValueError
        
    def _recover_light_wound(self, wound: LightWound, recovery_result: int):
        self._recover_wound(wound, recovery_result, 4, 10, 3)

    def _recover_medium_wound(self, wound: LightWound, recovery_result: int):
        self._recover_wound(wound, recovery_result, 6, 12, 3)

    def _recover_heavy_wound(self, wound: LightWound, recovery_result: int):
        self._recover_wound(wound, recovery_result, 9, 15, 3)

    def _recover_incapacitating_wound(self, wound: IncapacitatingWound, recovery_result: int):
        self._recover_wound(wound, recovery_result, 0, 9, -1)
    
    def recover_all_wounds_of_one_type(self,
            wound_list: Sequence[Wound],
            wound_recovery_function: Callable,
            wound_got_better_function: Callable,
            wound_got_worse_function: Callable,
            recovery_bonus: int,
            recovery_roll_results: Optional[int | Sequence[Optional[int]]] = None
        ) -> Sequence[Wound]:
        if not recovery_roll_results:
            recovery_roll_results = [None]*len(wound_list)
        if isinstance(recovery_roll_results, int):
            recovery_roll_results = [recovery_roll_results]*len(wound_list)
        for wound, roll_result in zip(wound_list, recovery_roll_results):
            try:
                roll_result = roll_result or am5_rolls.roll_stress()
                wound_recovery_function(wound, roll_result+recovery_bonus)
                if wound.status == WoundStatus.BETTER:
                    wound_got_better_function()
                elif wound.status == WoundStatus.WORSE:
                    wound_got_worse_function()
            except am5_rolls.BotchedRollExcption:
                wound.status = WoundStatus.WORSE
                wound_got_worse_function()
        return [wound for wound in self._light_wounds if wound.status == WoundStatus.SAME]

    def recover_all_light_wounds(self,
            recovery_bonus: int,
            recovery_roll_results: Optional[int | Sequence[Optional[int]]] = None
        ):
        remaining_light_wounds = self.recover_all_wounds_of_one_type(
            self._light_wounds,
            self._recover_light_wound,
            lambda x: x,
            self._add_medium_wound,
            recovery_bonus,
            recovery_roll_results
        )
        # this filtration is not necessary if everythign works right, but
        # if we don't do it the type checker will complain
        self._light_wounds = [wound for wound in remaining_light_wounds if isinstance(wound, LightWound)]

    def recover_all_medium_wounds(self,
            recovery_bonus: int,
            recovery_roll_results: Optional[int | Sequence[Optional[int]]] = None
        ):
        remaining_medium_wounds = self.recover_all_wounds_of_one_type(
            self._medium_wounds,
            self._recover_medium_wound,
            self._add_light_wound,
            self._add_heavy_wound,
            recovery_bonus,
            recovery_roll_results
        )
        self._medium_wounds = [wound for wound in remaining_medium_wounds if isinstance(wound, MediumWound)]

    def recover_all_heavy_wounds(self,
            recovery_bonus: int,
            recovery_roll_results: Optional[int | Sequence[Optional[int]]] = None
        ):
        remaining_heavy_wounds = self.recover_all_wounds_of_one_type(
            self._heavy_wounds,
            self._recover_medium_wound,
            self._add_medium_wound,
            self._add_incapacitating_wound,
            recovery_bonus,
            recovery_roll_results
        )
        self._heavy_wounds = [wound for wound in remaining_heavy_wounds if isinstance(wound, HeavyWound)]
    
    def recover_all_incapacitating_wounds(self,
            recovery_bonus: int,
            recovery_roll_results: Optional[int | Sequence[Optional[int]]] = None
        ):
        if self._incapacitating_wound:
            self.recover_all_wounds_of_one_type(
                [self._incapacitating_wound],
                self._recover_incapacitating_wound,
                self._add_heavy_wound,
                self._add_deadly_wound,
                recovery_bonus,
                recovery_roll_results
            )
