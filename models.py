from pydantic import BaseModel
from typing import Literal,Optional


PRIORITY_MAPPING = Literal["1", "2", "3","4",
                           "5", "6", "7", "8",
                           "9", "10", "11", "12",
                           "13", "14", "15", "16"]

OBJECT_TYPE_MAPPING = Literal["multiStateValue", "multiStateInput", "multiStateOutput",
                       "analogValue", "analogInput", "analogOutput",
                       "binaryValue", "binaryInput", "binaryOutput"]

BOOLEAN_ACTION_MAPPING = Literal["active", "inactive"]

class ValueModel(BaseModel):
    multiStateValue: Optional[int]
    multiStateInput: Optional[int]
    multiStateOutput: Optional[int]
    analogValue: Optional[int]
    analogInput: Optional[int]
    analogOutput: Optional[int]
    binaryValue: Optional[BOOLEAN_ACTION_MAPPING]
    binaryInput: Optional[BOOLEAN_ACTION_MAPPING]
    binaryOutput: Optional[BOOLEAN_ACTION_MAPPING]


class ReadRequestModel(BaseModel):
    address: str
    object_type: OBJECT_TYPE_MAPPING
    object_instance: int

class WriteRequestModel(BaseModel):
    address: str
    object_type: OBJECT_TYPE_MAPPING
    object_instance: int
    priority: PRIORITY_MAPPING
    
class ReleaseRequestModel(BaseModel):
    address: str
    object_type: OBJECT_TYPE_MAPPING
    object_instance: int
    priority: PRIORITY_MAPPING
    id: Optional[int]


