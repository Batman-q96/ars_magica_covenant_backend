"""Reputation is how well known you are ArM5(19)"""

from typing import Self
import pydantic


class Reputation(pydantic.BaseModel):
    """Reputation implementation class"""

    model_config = pydantic.ConfigDict(validate_assignment=True)
    score: int = pydantic.Field(default=1, ge=1)
    deeds: int = pydantic.Field(default=0, ge=0)
    content: str
    target: str

    @pydantic.model_validator(mode="after")
    def max_deeds(self) -> Self:
        """Validator to make sure reputable deeds never exceed those allowed by
        the current reputation score"""
        assert self.deeds < 5 * (self.score + 1)
        return self

    def add_deeds(self, deeds_gained: int) -> None:
        """Function to safely add deeds and increase reputation score if needed"""
        new_deeds = self.deeds + deeds_gained
        while new_deeds >= 5 * (self.score + 1):
            self.score += 1
            new_deeds = new_deeds - 5 * self.score
        self.deeds = new_deeds
