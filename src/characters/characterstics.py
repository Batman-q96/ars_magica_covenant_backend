import pydantic

class Characteristics(pydantic.BaseModel):
    strength: int = 0
    stamina: int = 0
    quickness: int = 0
    dexterity: int = 0
    intelligence: int = 0
    perception: int = 0
    presence: int = 0
    communication: int = 0
