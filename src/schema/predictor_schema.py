from typing import Dict, Any
from pydantic import BaseModel

class ModelRequest(BaseModel):
    input_data: Dict[str, Any]

    class Config:
        from_attributes = True  # Replace orm_mode
        model_config = {'protected_namespaces': ()}

class ChooseModelRequest(BaseModel):
    modelid: int

    class Config:
        from_attributes = True  # Replace orm_mode
        model_config = {'protected_namespaces': ()}

class UploadDataRequest(BaseModel):
    modelid: int
    data: Dict[str, Any]

    class Config:
        from_attributes = True  # Replace orm_mode
        model_config = {'protected_namespaces': ()}

class PredictionResult(BaseModel):
    class Config:
        from_attributes = True  # Replace orm_mode
        model_config = {'protected_namespaces': ()}
    age_group: str
