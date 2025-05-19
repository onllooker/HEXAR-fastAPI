from pydantic import BaseModel, ConfigDict
from typing import Optional

class SubstanceCreateSchema(BaseModel):
    name: str
    weight: float
    description: Optional[str]
    category_id: int

class SubstanceReadSchema(SubstanceCreateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int