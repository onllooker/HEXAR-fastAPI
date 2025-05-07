from pydantic import BaseModel

class SubstanceCrearteScheme(BaseModel):
    name: str
    weight: float

class SubstanceScheme(SubstanceCrearteScheme):
    id: int



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
