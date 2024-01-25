from __future__ import annotations
import pydantic

class Confidence(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(validate_assignment=True)
    points: int = pydantic.Field(default=0, ge=0)
    max: int = pydantic.Field(default=0, ge=0)

    @pydantic.model_validator(mode="after")
    def limit_confidence(self) -> Confidence:
        assert(self.points <= self.max)
        return self