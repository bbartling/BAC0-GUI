from typing import Any, AsyncIterator, Awaitable, Callable, Dict
from pydantic import BaseModel
from aiohttp_pydantic import PydanticView
from aiohttp import web

from models import ReadSingleModel,WriteSingleModel,ReleaseSingleModel
from models import ReadMultModel,WriteMultModel,ReleaseMultModel
from bacnet_actions import BacNetWorker


# Create your PydanticView and add annotations.
class ReadSingleView(PydanticView):
    async def get(self, bacnet_req: ReadSingleModel):
        read_result = await BacNetWorker.do_things(
        "read",
        bacnet_req.address,
        bacnet_req.object_type,
        bacnet_req.object_instance
        )
        response_obj = {"status":"read_success", "pv" : read_result}
        return web.json_response(response_obj)



class WriteSingleView(PydanticView):
    async def get(self, bacnet_req: WriteSingleModel):
        write_result = await BacNetWorker.do_things(
        "write",
        bacnet_req.address,
        bacnet_req.object_type,
        bacnet_req.object_instance,
        value = bacnet_req.value,
        priority = bacnet_req.priority
        )
        response_obj = {"status":"write_success", "info": write_result}
        return web.json_response(response_obj)
        
        
        
class ReleaseSingleView(PydanticView):
    async def get(self, bacnet_req: ReleaseSingleModel):
        release_result = await BacNetWorker.do_things(
        "release",
        bacnet_req.address,
        bacnet_req.object_type,
        bacnet_req.object_instance,
        priority = bacnet_req.priority
        )
        response_obj = {"status":"release_success", "info": release_result}
        return web.json_response(response_obj)



class ReadMultView(PydanticView):
    async def get(self, bacnet_req: ReadMultModel):
        device_mapping = {}
        data_as_dict = bacnet_req.dict()
        print("ReadMultView ",data_as_dict)
        
        for info,devices in data_as_dict.items():
            for device,attributes in devices.items():
                print(device)
                print(attributes)
                
                try:
                    read_result = await BacNetWorker.do_things(
                    "read",
                    attributes['address'],
                    attributes['object_type'],
                    attributes['object_instance']
                    )
                    
                    device_mapping[device] = {'pv':read_result}

                except:
                    device_mapping[device] = {'pv' : 'error'}

        response_obj = {"status":"read_success", "data": device_mapping }    
        return web.json_response(response_obj)



class WriteMultView(PydanticView):
    async def get(self, bacnet_req: WriteMultModel):
        device_mapping = {}
        data_as_dict = bacnet_req.dict()
        print("WriteMultView ",data_as_dict)
        
        for info,devices in data_as_dict.items():
            for device,attributes in devices.items():
                print(device)
                print(attributes)
                
                try:
                    write_result = await BacNetWorker.do_things(
                    "write",
                    attributes["address"],
                    attributes["object_type"],
                    attributes["object_instance"],
                    value = attributes["value"],
                    priority = attributes["priority"]
                    )
                    
                    device_mapping[device] = {attributes["object_type"] + ' ' + attributes["object_instance"] : write_result }
                    
                except:
                    device_mapping[device] = {attributes["object_type"] + ' ' + attributes["object_instance"] : 'error' }

        response_obj = {"status":"write_success", "data": device_mapping }    
        return web.json_response(response_obj)
        
        
        
class ReleaseMultView(PydanticView):
    async def get(self, bacnet_req: ReleaseMultModel):
        device_mapping = {}
        data_as_dict = bacnet_req.dict()
        print("ReleaseMultView ",data_as_dict)
        
        for info,devices in data_as_dict.items():
            for device,attributes in devices.items():
                print(device)
                print(attributes)
                
                try:
                    release_result = await BacNetWorker.do_things(
                    "release",
                    attributes["address"],
                    attributes["object_type"],
                    attributes["object_instance"],
                    priority = attributes["priority"]
                    )
                    
                    device_mapping[device] = {attributes["object_type"] + ' ' + attributes["object_instance"] : release_result }
                    
                except:
                    device_mapping[device] = {attributes["object_type"] + ' ' + attributes["object_instance"] : 'error' }

        response_obj = {"status":"release_success", "data": device_mapping }    
        return web.json_response(response_obj)













