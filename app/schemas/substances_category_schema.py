from pydantic import BaseModel, ConfigDict


class SubstanceCategoryCreateSchema(BaseModel):
    category_name: str
    description: str


class SubstanceCategoryReadSchema(SubstanceCategoryCreateSchema):
    model_config = ConfigDict(from_attributes=True)
    id: int
