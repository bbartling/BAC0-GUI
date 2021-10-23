# auto scan BACnet network


This is an experimental process to auto scan the LAN in the building for ALL BACnet devices to compile results into csv files and an SQLite db. Pip install these extra packages:

`$python3 -m pip install pandas`
`$python3 -m pip install numpy`
`$python3 -m pip install BAC0`
`$python3 -m pip install sqlalchemy`

* note these scripts in this directory CANNOT run at the same time as the aiohttp web app because of the BACnet process running. Only one BACnet instance can be used at a time on UDP port 47808 whether its the aiohttp restapi app or these auto scanning scripts.

Use a text editor to edit the `BACpypes.ini` file with the proper IP address of the machine running the scripts in this directory. The scripts here have no affect on the aiohttp web app, completely seperate process for auto scanning only.

Tested on python 3.9, run `$ python3 bac0WhoIs.py`



See the examples in this repo of the output files of `network_scan.csv` and `all_bacnet_bas.csv` for the desired output. The idea is to understand the BACnet network and devices faster that using the BAS or a 3rd party scanning tool.