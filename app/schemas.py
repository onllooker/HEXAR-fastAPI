from pydantic import BaseModel

class SubstanceScheme(BaseModel):
    name:str
    weight:float

class SynthesesScheme(BaseModel):
    name:str
    description:str

