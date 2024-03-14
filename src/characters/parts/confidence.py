"""Confidence is a character feature used to control luck see ArM5(19-20)"""

from typing import Self
import pydantic


class Confidence(pydantic.BaseModel):
    """Confidence points implementation as a class"""

    model_config = pydantic.ConfigDict(validate_assignment=True)
    points: int = pydantic.Field(default=0, ge=0)
    max: int = pydantic.Field(default=0, ge=0)

    @pydantic.model_validator(mode="after")
    def limit_confidence(self) -> Self:
        """Validator for confidence points to make sure they don't exceed the max"""
        assert self.points <= self.max
        return self
