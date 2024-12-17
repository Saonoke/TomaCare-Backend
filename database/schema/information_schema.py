from pydantic import BaseModel

class InformationResponse(BaseModel):
    id: int
    title: str
    content: str
    medicine: str
    type:str
