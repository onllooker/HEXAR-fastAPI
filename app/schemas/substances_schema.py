from typing import Optional

from pydantic import BaseModel, ConfigDict


class SubstanceCreateSchema(BaseModel):
    name: str
    weight: float
    description: Optional[str]
    category_id: int


class SubstanceReadSchema(SubstanceCreateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
