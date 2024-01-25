from __future__ import annotations
import pydantic

class Reputation(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(validate_assignment=True)
    score: int = pydantic.Field(default=1, ge=1)
    deeds: int = pydantic.Field(default=0, ge=0)
    content: str
    target: str

    @pydantic.model_validator(mode="after")
    def max_deeds(self) -> Reputation:
        assert(self.deeds < 5*(self.score+1))
        return self

    def add_deeds(self, deeds_gained: int) -> None:
        new_deeds = self.deeds + deeds_gained
        while new_deeds >= 5*(self.score+1):
            self.score += 1
            new_deeds = new_deeds - 5*self.score
        self.deeds = new_deeds
