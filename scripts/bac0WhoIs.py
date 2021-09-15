import BAC0, time
import glob, os
import time, datetime
import logging
import pandas as pd
from sqlalchemy import create_engine


# delete db from previous run if a fresh one is needed
delete_db = glob.glob('./*.db')
for d in delete_db:
    os.remove(d)

# delete db from previous run if a fresh one is needed
delete_csv = glob.glob('./*.csv')
for c in delete_csv:
    os.remove(c)


# delete log files from previous run for fresh ones
delete_logs = glob.glob('./bacpypes_logs/*.log')
for l in delete_logs:
    os.remove(l)


# delete log files from previous run for fresh ones
delete_BAC0_logs = glob.glob('./logs_whoIsBACO.log')
for b in delete_BAC0_logs:
    os.remove(b)




logging.basicConfig(filename='logs_whoIsBACO.log',level=logging.INFO,format= '%(asctime)s - %(levelname)s: %(message)s',\
                     datefmt = '%m/%d/%Y %I:%M:%S %p' )
bacnet = BAC0.lite()

print("old bacpypes log removed")
logging.info("old bacpypes log removed")
print("old db removed")
logging.info("old db removed")


# scan network
time.sleep(1)
devices = bacnet.whois(global_broadcast=True)
device_mapping = {}
for device in devices:
    if isinstance(device, tuple):
        device_mapping[device[1]] = device[0]
        print("Detected device %s with address %s" % (str(device[1]), str(device[0])))
        
print(device_mapping)
logging.info(device_mapping)

device_count = f"{str(len(device_mapping))} devices discovered on network"
print(device_count)
logging.info(device_count)

# shut down BAC0 so we can use bacpypes
bacnet.disconnect()
print("BAC0 disconnected")
logging.info("BAC0 disconnected")
time.sleep(5)

df = pd.DataFrame(devices,columns=["address", "bacnetId"])
print(df)

df.to_csv('network_scan.csv')

engine = create_engine('sqlite:///all_bacnet_bas.db', echo=True)
sqlite_connection = engine.connect()
sqlite_table = "bacnet_whois"
df.to_sql(sqlite_table, sqlite_connection, if_exists='replace')
sqlite_connection.close()
print("Data saved to sql!")


add_port_device_mapping = {}
for device_id,address in device_mapping.items():
    if address.count('.') == 3:
        add_port_device_mapping[device_id] = f'{address}:47808'
    else:
        add_port_device_mapping[device_id] = address
        
print(add_port_device_mapping)
logging.info(add_port_device_mapping)

lets_go = f"Lets GO!, {time.ctime()}"
print(lets_go)
logging.info(lets_go)

start_calc = datetime.datetime.now()

try:
    # py -3.9 ReadObjectList.py 1002 10.200.200.32:47808
    # in Windows terminal to run the .py file
    for device_id,address in add_port_device_mapping.items():
    
        going_to_try = f'GOING TO TRY: {device_id} {address}'
        print(going_to_try)
        logging.info(going_to_try)
        
        os.system(f'py -3.9 ReadObjectList.py {device_id} {address}')
        
        success = f'OS ran {device_id} {address}'
        print(success)
        logging.info(success)
        
        time.sleep(1)

except KeyboardInterrupt:
    pass

finally:
    done_deal = f"Done deal..., {time.ctime()}"
    print(done_deal)
    logging.info(done_deal)

    end_calc = datetime.datetime.now()
    diff = (end_calc - start_calc)   
    diff_seconds = int(diff.total_seconds())
    minute_seconds, seconds = divmod(diff_seconds, 60)
    hours, minutes = divmod(minute_seconds, 60)
    
    hms = f"{hours}h {minutes}m {seconds}s"
    print(hms)
    logging.info(hms)
