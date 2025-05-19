from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from substances_schema import SubstanceReadSchema


class RecipeCreateSchema(BaseModel):
    substance_id: int
    percent: float

class RecipeReadSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    substance: SubstanceReadSchema
    percent: float

class SynthesesCreateSchema(BaseModel):
    name:str
    description:Optional[str]
    recipe: List[RecipeCreateSchema] = []

class SynthesesReadSchema(SynthesesCreateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
    recipe: List[RecipeReadSchema]