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
        action = "read",
        dev_address = bacnet_req.address,
        object_type = bacnet_req.object_type,
        object_instance = bacnet_req.object_instance
        )
        return web.json_response(read_result)



class WriteSingleView(PydanticView):

    async def get(self, bacnet_req: WriteSingleModel):
        write_result = await BacNetWorker.do_things(
        action = "write",
        dev_address = bacnet_req.address,
        object_type = bacnet_req.object_type,
        object_instance = bacnet_req.object_instance,
        value = bacnet_req.value,
        priority = bacnet_req.priority
        )
        return web.json_response(write_result)
        
        
        
class ReleaseSingleView(PydanticView):

    async def get(self, bacnet_req: ReleaseSingleModel):
        release_result = await BacNetWorker.do_things(
        action = "release",
        dev_address = bacnet_req.address,
        object_type = bacnet_req.object_type,
        object_instance = bacnet_req.object_instance,
        priority = bacnet_req.priority
        )
        return web.json_response(release_result)



class ReadMultView(PydanticView):

    async def get(self, bacnet_req: ReadMultModel):
        final_resp = []
        data_as_dict = bacnet_req.dict()
        print("ReadMultView ",data_as_dict)
        
        for obj in data_as_dict.values():
            for point in obj:

                read_result = await BacNetWorker.do_things(
                action = "read",
                dev_address = point['address'],
                object_type = point['object_type'],
                object_instance = point['object_instance']
                )
                
                final_resp.append(read_result)
        return web.json_response(final_resp)



class WriteMultView(PydanticView):

    async def get(self, bacnet_req: WriteMultModel):
        final_resp = []
        data_as_dict = bacnet_req.dict()
        print("WriteMultView ",data_as_dict)
        
        for obj in data_as_dict.values():
            for point in obj:
                
                write_result = await BacNetWorker.do_things(
                action = "write",
                dev_address = point["address"],
                object_type = point["object_type"],
                object_instance = point["object_instance"],
                value = point["value"],
                priority = point["priority"]
                )
                    
                final_resp.append(write_result)
        return web.json_response(final_resp)
        
        
        
class ReleaseMultView(PydanticView):
    async def get(self, bacnet_req: ReleaseMultModel):

        final_resp = []
        data_as_dict = bacnet_req.dict()
        print("ReleaseMultView ",data_as_dict)

        for obj in data_as_dict.values():
            for point in obj:
                
                release_result = await BacNetWorker.do_things(
                action = "release",
                dev_address = point["address"],
                object_type = point["object_type"],
                object_instance = point["object_instance"],
                priority = point["priority"]
                )
                

                final_resp.append(release_result)
        return web.json_response(final_resp)










