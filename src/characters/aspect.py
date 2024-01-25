from typing import Literal, Iterable

import pydantic

class Aspect(pydantic.BaseModel):
    name: str
    scale: Literal["Minor", "Major"]
    tag: Literal["Hermetic", "Supernatural", "Social Status", "General"]
    content: str

class Virtue(Aspect):
    pass

class Flaw(Aspect):
    tag: Literal["Hermetic", "Personality", "Story", "Supernatural", "Social Status", "General"]