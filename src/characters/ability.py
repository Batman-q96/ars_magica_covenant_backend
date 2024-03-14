"""Abilities are skills that characters have, both magical and non magical see ArM5(62-67)"""

# from __future__ import annotations
from typing import Self
import pydantic


class Ability(pydantic.BaseModel):
    """Ability implementation"""

    model_config = pydantic.ConfigDict(validate_assignment=True)
    name: str
    level: int = pydantic.Field(default=0)
    experience: int = pydantic.Field(default=0, ge=0)

    @pydantic.model_validator(mode="after")
    def max_experience(self) -> Self:
        """Validator to make sure experience isn't too high for level"""
        assert self.experience < 5 * (self.level + 1)
        return self

    def add_experience(self, exp_to_gain: int) -> None:
        """Safely add experience potentially increasing level if needed"""
        new_experience = self.experience + exp_to_gain
        while new_experience >= 5 * (self.level + 1):
            self.level += 1
            new_experience = new_experience - 5 * self.level
        self.experience = new_experience
