from pydantic import BaseModel

class ResolvedPeriod(BaseModel):
    id: int
    label: str
    value: str   
    type: str    