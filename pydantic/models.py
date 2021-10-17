from typing import Any, AsyncIterator, Awaitable, Callable, Dict
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
    devices: Dict[str, ReadSingleModel]


class WriteMultModel(BaseModel):
    devices: Dict[str, WriteSingleModel]


class ReleaseMultModel(BaseModel):
    devices: Dict[str, ReleaseSingleModel]







