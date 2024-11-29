from pydantic import BaseModel

class MachineLearningResponse(BaseModel):
    predicted_class: str
    disease_id : int | None = None
    percentage:int | None = None

