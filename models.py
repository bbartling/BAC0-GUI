from typing import Union, List
from pydantic import BaseModel



# Use pydantic BaseModel to validate request body
class ReadSingleModel(BaseModel):
    address: str
    object_type: str
    object_instance: str


class WriteSingleModel(BaseModel):
    address: str
    object_type: str
    object_instance: str
    value: str
    priority: str

    
class ReleaseSingleModel(BaseModel):
    address: str
    object_type: str
    object_instance: str
    priority: str
    
    
class ReadMultModel(BaseModel):
    read: List[ReadSingleModel]

class WriteMultModel(BaseModel):
    write: List[WriteSingleModel]

class ReleaseMultModel(BaseModel):
    release: List[ReleaseSingleModel]















