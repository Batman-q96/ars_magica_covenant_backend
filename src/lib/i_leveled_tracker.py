"""A leveled tracker si anything that can accumulate points and level up,
including things like abilities, arts, reputations etc."""

# from __future__ import annotations
from typing import Self
import abc

import pydantic


class ILeveledTracker(pydantic.BaseModel):
    """LeveledTracker interface definition"""

    model_config = pydantic.ConfigDict(validate_assignment=True)
    name: str
    level: int = pydantic.Field(default=0)
    points: int = pydantic.Field(default=0)

    @pydantic.model_validator(mode="after")
    def max_points(self) -> Self:
        """Validator to make sure points don't exceed the level.
        ex. for arts points should be < (level+1)"""
        raise NotImplementedError("This method should be implemented in subclasses")

    @abc.abstractmethod
    def add_points(self, points_to_gain: int) -> None:
        """Safely add experience potentially increasing level if needed"""
        raise NotImplementedError("This method should be implemented in subclasses")
