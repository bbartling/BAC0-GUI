import BAC0
import time
from aiohttp_pydantic import PydanticView


# define BAC0 app
#STATIC_BACNET_IP = '192.168.0.103/24'
#bacnet = BAC0.lite(IP=STATIC_BACNET_IP)
bacnet = BAC0.lite()

# BACnet scan network
time.sleep(1)
'''
devices = bacnet.whois(global_broadcast=True)
device_mapping = {}
for device in devices:
    if isinstance(device, tuple):
        device_mapping[device[1]] = device[0]
        print("Detected device %s with address %s" % (str(device[1]), str(device[0])))
print(device_mapping)
print((str(len(device_mapping)) + " devices discovered on network."))
'''

# Create your PydanticView and add annotations.
class BacNetWorker(PydanticView):
    async def do_things(**kwargs):

        action = kwargs.get('action', None)
        address = kwargs.get('dev_address', None)
        object_type = kwargs.get('object_type', None)
        object_instance = kwargs.get('object_instance', None)
        value = kwargs.get('value', None)
        priority = kwargs.get('priority', None)

        if action == "read":
            try:
                read_vals = f'{address} {object_type} {object_instance} presentValue'
                read_result = bacnet.read(read_vals)
                print("Excecuting BACnet read statement: ", read_vals," : ",read_result)
                if isinstance(read_result, str):
                    pass
                else:
                    read_result = round(read_result,2)
                return read_result
            except Exception as error:
                return f"error: {error}"
      

        elif action == "write":
            try:
                write_vals = f'{address} {object_type} {object_instance} presentValue {value} - {priority}'
                bacnet.write(write_vals)
                print("Excecuting BACnet write statement: ", write_vals)
                return "success"          
            except Exception as error:
                return f"error: {error}"


        elif action == "release":
            try:    
                release_vals = f'{address} {object_type} {object_instance} presentValue null - {priority}'
                print("Excecuting BACnet release statement:", release_vals)
                bacnet.write(release_vals)
                return "success" 
            except Exception as error:
                return f"error: {error}"
                

        elif action == "kill_switch":
            try:    
                bacnet.disconnect()
                return "success"
            except Exception as error:
                return f"error! - {error}"
                
        else:
            return "BACnet server error"


