"""Wounding is the consequence of damage Arm5(178-180)"""

from typing import Optional, Callable, Sequence, ClassVar
import math
from dateutil import relativedelta

import pydantic

from characters.parts.wounds import fatal_wound
from lib import am5_rolls

from src.characters.parts.wounds import (
    light_wound,
    medium_wound,
    heavy_wound,
    incapacitating_wound,
    fatal_wound,
    i_wound,
    wound_status,
)


class WoundTracker(pydantic.BaseModel):
    """Class to track wounds on a character"""

    _modified_size: int
    _light_wounds: list[light_wound.LightWound] = []
    _medium_wounds: list[medium_wound.MediumWound] = []
    _heavy_wounds: list[heavy_wound.HeavyWound] = []
    _incapacitating_wound: Optional[incapacitating_wound.IncapacitatingWound] = None
    _fatal_wound: Optional[fatal_wound.FatalWound] = None

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
    def _add_light_wound(self) -> light_wound.LightWound:
        wound = light_wound.LightWound()
        self._light_wounds.append(wound)
        return wound

    def _add_medium_wound(self) -> medium_wound.MediumWound:
        wound = medium_wound.MediumWound()
        self._medium_wounds.append(wound)
        return wound

    def _add_heavy_wound(self) -> heavy_wound.HeavyWound:
        wound = heavy_wound.HeavyWound()
        self._heavy_wounds.append(wound)
        return wound

    def _add_incapacitating_wound(self) -> incapacitating_wound.IncapacitatingWound:
        wound = incapacitating_wound.IncapacitatingWound()
        self._incapacitating_wound = wound
        return wound

    def _add_fatal_wound(self) -> fatal_wound.FatalWound:
        wound = fatal_wound.FatalWound()
        self._fatal_wound = wound
        return wound

    def add_wound(self, wound: i_wound.IWound) -> None:
        """Add a wound of a particular type"""
        if isinstance(wound, light_wound.LightWound):
            self._light_wounds.append(wound)
        elif isinstance(wound, medium_wound.MediumWound):
            self._medium_wounds.append(wound)
        elif isinstance(wound, heavy_wound.HeavyWound):
            self._heavy_wounds.append(wound)
        elif isinstance(wound, incapacitating_wound.IncapacitatingWound):
            self._incapacitating_wound = wound
        elif isinstance(wound, fatal_wound.FatalWound):
            self._fatal_wound = wound
        else:
            raise TypeError

    def take_damage(self, damage: int) -> i_wound.IWound:
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
