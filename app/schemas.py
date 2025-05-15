from pydantic import BaseModel


class SubstanceCreateScheme(BaseModel):
    name: str
    weight: float
    category_id: int


class SubstanceScheme(SubstanceCreateScheme):
    id: int


class SynthesesCreateScheme(BaseModel):
    name: str
    description: str


class SynthesesScheme(SynthesesCreateScheme):
    id: int


class SubstanceCategoryCreateScheme(BaseModel):
    category_name: str
    description: str


class SubstanceCategoryScheme(SubstanceCategoryCreateScheme):
    id: int
