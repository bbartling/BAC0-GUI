import BAC0,time,json 
from aiohttp.web import Application, json_response, middleware
import asyncio
from pathlib import Path
from typing import Any, AsyncIterator, Awaitable, Callable, Dict
from aiohttp_pydantic import PydanticView
from pydantic import BaseModel
from aiohttp import web
from aiohttp_pydantic import oas


# define BAC0 app
#STATIC_BACNET_IP = '192.168.0.103/24'
#bacnet = BAC0.lite(IP=STATIC_BACNET_IP)
bacnet = BAC0.lite()

# BACnet scan network
time.sleep(1)
devices = bacnet.whois(global_broadcast=True)
device_mapping = {}
for device in devices:
    if isinstance(device, tuple):
        device_mapping[device[1]] = device[0]
        print("Detected device %s with address %s" % (str(device[1]), str(device[0])))
print(device_mapping)
print((str(len(device_mapping)) + " devices discovered on network."))


@middleware
async def _not_found_to_404(request, handler):
    try:
        return await handler(request)
    except Model.NotFound as key:
        return json_response({"error": f"Pet {key} does not exist"}, status=404)


app = Application(middlewares=[_not_found_to_404])
oas.setup(app, version_spec="1.0.1", title_spec="BACnet Rest API App")


async def bacnet_ops(action,address,object_type,object_instance, **kwargs):
    value = kwargs.get('value', None)
    priority = kwargs.get('priority', None)

    if action == "read":
        try:
            read_vals = f'{address} {object_type} {object_instance} presentValue'
            print("Excecuting BACnet read statement:", read_vals)
            read_result = bacnet.read(read_vals)
            read_result_round = round(read_result,2)
            return read_result_round
        except Exception as error:
            return "error"
  
    elif action == "write":
        try:
            write_vals = f'{address} {object_type} {object_instance} presentValue {value} - {priority}'
            print("Excecuting BACnet write statement:", write_vals)
            bacnet.write(write_vals)
            return write_vals          
        except Exception as error:
            return "error"

    elif action == "release":
        try:    
            release_vals = f'{address} {object_type} {object_instance} presentValue null - {priority}'
            print("Excecuting BACnet release statement:", release_vals)
            bacnet.write(release_vals)
            return release_vals 
        except Exception as error:
            return "error"
            
    else:
        return "server error on BACnet opts"




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
    
    
'''
class ReadMultModel(BaseModel):
    name: str
    nb_page: Optional[int]

class WriteMultModel(BaseModel):
    name: str
    nb_page: Optional[int]
    
class ReleaseMultModel(BaseModel):
    name: str
    nb_page: Optional[int]

'''


# Create your PydanticView and add annotations.
class ReadSingleView(PydanticView):
    async def get(self, bacnet_req: ReadSingleModel):
        read_result = await bacnet_ops(
        "read",
        bacnet_req.address,
        bacnet_req.object_type,
        bacnet_req.object_instance
        )
        response_obj = {"status":"success", "present_value" : read_result}
        return web.json_response(response_obj)


class WriteSingleView(PydanticView):
    async def get(self, bacnet_req: WriteSingleModel):
        write_result = await bacnet_ops(
        "write",
        bacnet_req.address,
        bacnet_req.object_type,
        bacnet_req.object_instance,
        value = bacnet_req.value,
        priority = bacnet_req.priority
        )
        response_obj = {"status":"success", "info": write_result}
        return web.json_response(response_obj)
        
        
class ReleaseSingleView(PydanticView):
    async def get(self, bacnet_req: ReleaseSingleModel):
        release_result = await bacnet_ops(
        "release",
        bacnet_req.address,
        bacnet_req.object_type,
        bacnet_req.object_instance,
        priority = bacnet_req.priority
        )
        response_obj = {"status":"success", "info": release_result}
        return web.json_response(response_obj)



'''

#READ MULTIPLE
@router.get('/bacnet/read/multiple')
async def reader_mult(request: web.Request) -> web.Response:

    json_data = await request.json()
    device_mapping = {}

    try:
        for device,values in json_data.items():
            address = values["address"]
            object_type = values["object_type"]
            object_instance = values["object_instance"]
            read_vals = f'{address} {object_type} {object_instance} presentValue'
            print("Excecuting read multiple statement:", read_vals)
            read_result = bacnet.read(read_vals)
            read_result_round = round(read_result,2)
            device_mapping[device] = {'pv':read_result_round}

    except:
        device_mapping[device] = {'pv' : 'error'}

    response_obj = { 'status' : 'success', 'data' : device_mapping }    
    return web.json_response(response_obj)



#WRITE MULTIPLE
@router.get('/bacnet/write/multiple')
async def writer_mult(request: web.Request) -> web.Response:

    json_data = await request.json()
    device_mapping = {}

    try:
        for device,values in json_data.items():
            address = values["address"]
            object_type = values["object_type"]
            object_instance = values["object_instance"]
            value = values["value"]
            priority = values["priority"]
        
            write_vals = f'{address} {object_type} {object_instance} presentValue {value} - {priority}'
            print("Excecuting Write Mult Statement:", write_vals)
            bacnet.write(write_vals)
            device_mapping[device] = {object_type + ' ' + object_instance : value }

    except:
        device_mapping[device] = {object_type + ' ' + object_instance : 'error' }

    response_obj = { 'status' : 'success', 'info' : device_mapping }
    return web.json_response(response_obj)        





#RELEASE MULTIPLE
@router.get('/bacnet/release/multiple')
async def releaser_mult(request: web.Request) -> web.Response:

    json_data = await request.json()
    device_mapping = {}

    try:
        for device,values in json_data.items():
            print(device)
            print(values)
            address = values["address"]
            object_type = values["object_type"]
            object_instance = values["object_instance"]
            priority = values["priority"]
        
            write_vals = f'{address} {object_type} {object_instance} presentValue null - {priority}'
            print("Excecuting Release Mult Statement:", write_vals)
            bacnet.write(write_vals)
            device_mapping[device] = {object_type + ' ' + object_instance : 'success'}

    except:
        device_mapping[device] = {object_type + ' ' + object_instance : 'error'}

    response_obj = { 'status' : 'success', 'release_info' : device_mapping }
    return web.json_response(response_obj)         


'''


app.router.add_view('/bacnet/read/single', ReadSingleView)
app.router.add_view('/bacnet/write/single', WriteSingleView)
app.router.add_view('/bacnet/release/single', ReleaseSingleView)
web.run_app(app, host='0.0.0.0', port=8080)





