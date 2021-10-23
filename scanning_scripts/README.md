# auto scan BACnet network


This is an experimental process to auto scan the LAN in the building for ALL BACnet devices to compile results into csv files and an SQLite db. 

`pip install pandas`
`pip install numpy`
`pip install BAC0`
`pip install sqlalchemy`


Tested on python 3.9, run `$ python3 bac0WhoIs.py`



See the examples in this repo of the output files of `network_scan.csv` and `all_bacnet_bas.csv` for the desired output. The idea is to understand the BACnet network and devices faster that using the BAS or a 3rd party scanning tool.