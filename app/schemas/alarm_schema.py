from pydantic import BaseModel

class AlarmCreateScheme(BaseModel):
    message: str
    timestamp: str
class AlarmScheme(AlarmCreateScheme):
    id: int

