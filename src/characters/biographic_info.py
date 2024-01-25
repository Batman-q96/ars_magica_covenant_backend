import pydantic

class BiographicInfo(pydantic.BaseModel):
    gender: str = ''
    nationality: str = ''
    origin: str = ''
    religion: str = ''
    height: str = ''
    weight: str = ''
    hair: str = ''
    eyes: str = ''
    handedness: str = ''