"""Biographic info is character info that is not mechanically reelvant but is 
relelvant to the character overall"""

import pydantic


class BiographicInfo(pydantic.BaseModel):
    """A container class for biographic info"""

    gender: str = ""
    nationality: str = ""
    origin: str = ""
    religion: str = ""
    height: str = ""
    weight: str = ""
    hair: str = ""
    eyes: str = ""
    handedness: str = ""
    description: str = ""
