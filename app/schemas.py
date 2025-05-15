from pydantic import BaseModel, Field

class SubstanceCreateScheme(BaseModel):
    name: str
    weight: float
    category_id: int
class SubstanceScheme(SubstanceCreateScheme):
    id: int

    class Config:
        orm_mode = True


class SynthesesCreateScheme(BaseModel):
    name:str
    description:str
class SynthesesScheme(SynthesesCreateScheme):
    id: int


class SubstanceCategoryCreateScheme(BaseModel):
    category_name: str
    description: str
class SubstanceCategoryScheme(SubstanceCategoryCreateScheme):
    id: int


class AlarmCreateScheme(BaseModel):
    message: str
    timestamp: str
class AlarmScheme(AlarmCreateScheme):
    id: int

