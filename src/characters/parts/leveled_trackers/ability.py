"""Abilities are skills that characters have, both magical and non magical see ArM5(62-67)"""

from typing import Self
import pydantic

from characters.parts.leveled_trackers import i_leveled_tracker


class Ability(i_leveled_tracker.ILeveledTracker):
    """Ability implementation"""

    points: int = pydantic.Field(default=0, alias="experience", ge=0)
    specialization: str

    @pydantic.model_validator(mode="after")
    def max_points(self) -> Self:
        """Validator to make sure experience isn't too high for level"""
        assert self.points < 5 * (self.level + 1)
        return self

    def add_points(self, points_to_gain: int) -> None:
        """Alias for add_experience to match interface"""
        self.add_points(points_to_gain)

    def add_experience(self, exp_to_gain: int) -> None:
        """Safely add experience potentially increasing level if needed"""
        new_points = self.points + exp_to_gain
        while new_points >= 5 * (self.level + 1):
            self.level += 1
            new_points = new_points - 5 * self.level
        self.points = new_points
