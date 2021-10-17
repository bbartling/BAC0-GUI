import BAC0,time,json 
from aiohttp.web import Application, json_response, middleware
import asyncio
from pathlib import Path
from aiohttp_pydantic import PydanticView
from aiohttp import web
from aiohttp_pydantic import oas
from models import ReadSingleModel,WriteSingleModel,ReleaseSingleModel
from models import ReadMultModel
from random import randrange


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


'''
@middleware
async def _not_found_to_404(request, handler):
    try:
        return await handler(request)
    #except Model.NotFound as key:
        #return json_response({"error": f"{key} does not exist"}, status=404)
    except:
        return json_response({"error": f"key does not exist"}, status=404)


app = Application(middlewares=[_not_found_to_404])
'''

app = Application()
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



class ReadMultView(PydanticView):
    async def get(self, bacnet_req: ReadMultModel):
        device_mapping = {}
        data_as_dict = bacnet_req.dict()
        
        for info,devices in data_as_dict.items():
            for device,attributes in devices.items():
                print(device)
                print(attributes)
                
                try:
                    read_result = await bacnet_ops(
                    "read",
                    attributes['address'],
                    attributes['object_type'],
                    attributes['object_instance']
                    )
                    
                    device_mapping[device] = {'pv':read_result}

                except:
                    device_mapping[device] = {'pv' : 'error'}

        response_obj = {"status":"success", "data": device_mapping }    
        return web.json_response(response_obj)


class WriteMultView(PydanticView):
    async def get(self, bacnet_req: WriteMultModel):
        device_mapping = {}
        data_as_dict = bacnet_req.dict()
        
        for info,devices in data_as_dict.items():
            for device,attributes in devices.items():
                print(device)
                print(attributes)
                
                try:
                    write_result = await bacnet_ops(
                    "write",
                    bacnet_req.address,
                    bacnet_req.object_type,
                    bacnet_req.object_instance,
                    value = bacnet_req.value,
                    priority = bacnet_req.priority
                    )
                    
                    device_mapping[device] = {'pv':write_result}
                    device_mapping[device] = {bacnet_req.object_type + ' ' + bacnet_req.object_instance : value }
                    
                except:
                    device_mapping[device] = {bacnet_req.object_type + ' ' + bacnet_req.object_instance : 'error' }

        response_obj = {"status":"success", "data": device_mapping }    
        return web.json_response(response_obj)
        
        
        
class ReleaseMultView(PydanticView):
    async def get(self, bacnet_req: ReleaseMultModel):
        device_mapping = {}
        data_as_dict = bacnet_req.dict()
        
        for info,devices in data_as_dict.items():
            for device,attributes in devices.items():
                print(device)
                print(attributes)
                
                try:
                    release_result = await bacnet_ops(
                    "release",
                    bacnet_req.address,
                    bacnet_req.object_type,
                    bacnet_req.object_instance,
                    priority = bacnet_req.priority
                    )
                    
                    device_mapping[device] = {object_type + ' ' + object_instance : 'error'}

                except:
                    device_mapping[device] = {bacnet_req.object_type + ' ' + bacnet_req.object_instance : 'error'}

        response_obj = {"status":"success", "data": device_mapping }    
        return web.json_response(response_obj)



app.router.add_view('/bacnet/read/single', ReadSingleView)
app.router.add_view('/bacnet/read/multiple', ReadMultView)
app.router.add_view('/bacnet/write/single', WriteSingleView)
app.router.add_view('/bacnet/write/multiple', WriteMultView)
app.router.add_view('/bacnet/release/single', ReleaseSingleView)
app.router.add_view('/bacnet/release/multiple', ReleaseMultView)
web.run_app(app, host='0.0.0.0', port=8080)





