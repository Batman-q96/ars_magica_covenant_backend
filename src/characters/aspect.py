"""Aspects are virtues and flaws see ArM5(36-61)"""

from typing import Literal

import pydantic


class Aspect(pydantic.BaseModel):
    """The general base class for both virtues and flaws"""

    name: str
    scale: Literal["Minor", "Major"]
    tag: Literal["Hermetic", "Supernatural", "Social Status", "General"]
    content: str


class Virtue(Aspect):
    """Virtues are positive aspects"""


class Flaw(Aspect):
    """Flaws are negative aspects"""

    tag: Literal[
        "Hermetic", "Personality", "Story", "Supernatural", "Social Status", "General"
    ]
