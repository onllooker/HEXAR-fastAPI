from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from .substances_schema import SubstanceReadSchema


class RecipeCreateSchema(BaseModel):
    substance_id: int
    percent: float


class RecipeReadSchema(BaseModel):
    substance: SubstanceReadSchema
    percent: float

    model_config = ConfigDict(from_attributes=True)


class SynthesisCreateSchema(BaseModel):
    name: str
    description: Optional[str]
    recipe: List[RecipeCreateSchema] = Field(default_factory=list)


class SynthesisReadSchema(SynthesisCreateSchema):
    id: int
    recipe: List[RecipeReadSchema]

    model_config = ConfigDict(from_attributes=True)
