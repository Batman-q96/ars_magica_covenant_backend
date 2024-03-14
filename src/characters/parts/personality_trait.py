"""Personality traits are descriptors that help guide roleplaying a character ArM5(18-19)"""

import pydantic


class PersonalityTrait(pydantic.BaseModel):
    """Class to define a personality trait"""

    name: str
    intensity: int = pydantic.Field(ge=-3, le=3)
