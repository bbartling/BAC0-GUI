import BAC0
import time
from aiohttp_pydantic import PydanticView


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


# Create your PydanticView and add annotations.
class BACnetActions(PydanticView):
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


