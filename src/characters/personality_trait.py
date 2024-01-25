import pydantic

class PersonalityTrait(pydantic.BaseModel):
    name: str
    intensity: int = pydantic.Field(ge=-3, le=3)
