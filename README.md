# bacnet-restapi

This is a RESTful interface to retrieve data from BACnet building automation systems (BAS) with typical industry standard BACnet read, writes, and release commands. The idea is to run this app along side the BAS on a buildings LAN which is NOT a cloud environment.


## Overview

- .gitignore
- flaskapp.py
- README.md
- requirements.txt
- runtime.txt


## Requirements

See requirements.txt.


## Installation & Usage

```bash
$ git clone https://github.com/bbartling/bacnet-restapi.git
# Or using downloaded zip file 
$ unzip bacnet-restapi.zip

# change the directory
$ cd bacnet-restapi

# create virtual enviornment
$ python3 -m venv env

# activate virtual enviornment
$ source env/bin/activate

# install packages
$ pip3 install -r requirements.txt

# start the restapi web app
$ python3 aioapp.py
```

On startup BAC0 performs a BACnet "whois" where the screenshot below shows 2 BACnet devices that replied. Device `192.168.0.190` is an IP based BACnet device and device `201201` (BACnet instance ID) on MSTP network `12345` with hardware address `2` shown. This App supports both MSTP devices and IP based BACnet controllers.
![Start Up](/images/startup.PNG)


# [Swagger](https://swagger.io/resources/open-api/) for OpenAPI rest endpoints:
After app starts go to the device URL: [http://127.0.0.1:8080/oas](http://127.0.0.1:8080/oas) to bring up a page that looks like this below:
![Swagger1](/images/swagger1.PNG)

[Pydantic Models](https://pydantic-docs.helpmanual.io/usage/models/) for BACnet requests with BAC0 which is also built into the swagger documentation mentioned above:
![Swagger2](/images/swagger2.PNG)


# Example `GET` requests to the restapi app with JSON in body:

BACnet Write Single:
`192.168.0.105:5000/bacnet/read/single`

```
{
	"address":"12345:2",
	"object_type":"analogInput",
	"object_instance":"2"
}
```

BACnet Write Multiple:
`192.168.0.105:5000/bacnet/read/multiple`

```
{"devices":{
    "boiler":{
    "address":"12345:2",
    "object_type":"analogInput",
    "object_instance":"2"
    },
    "cooling_plant":{
    "address":"12345:2",
    "object_type":"analogInput",
    "object_instance":"2"
    },
    "air_handler_1":{
    "address":"12345:2",
    "object_type":"analogInput",
    "object_instance":"2"
    },
    "air_handler_2":{
    "address":"12345:2",
    "object_type":"analogInput",
    "object_instance":"2"
    },
    "hot_water_valve_1":{
    "address":"12345:2",
    "object_type":"analogInput",
    "object_instance":"2"
    }
}}
```

returned JSON:

```
{
  "status": "read_success",
  "data": {
    "boiler": {
      "pv": 67.31
    },
    "cooling_plant": {
      "pv": 67.31
    },
    "air_handler_1": {
      "pv": 67.31
    },
    "air_handler_2": {
      "pv": 67.31
    },
    "hot_water_valve_1": {
      "pv": 67.31
    }
  }
}
```

App also supports BACnet writes and releases, see BAC0 documention for what is going under the hood of the aiohttp web app on the BACnet side:
https://bac0.readthedocs.io/en/latest/

# Note about Rasp pi Buster:
Use the [flask_version](https://github.com/bbartling/bacnet-restapi/tree/main/flask_version) if running python 3.7 or default rasp pi Buster image. This has been tested on a rasp pi Buster image with upgrading Python to 3.9 using this tutorial:
https://itheo.tech/ultimate-python-installation-on-a-raspberry-pi-ubuntu-script


## Node Red Example Flows
[Link for example flows](https://github.com/bbartling/flask-restul-bacnet/tree/main/example-node-red-flows)
![node_red](/images/node_red_flows.PNG)


## Issues and comments
Please submit git issues to improve app as well as bugs found during testing. 


## Inspiration
The idea for this tool is from the VOLTTRON platform developed by PNNL on the BACnet features with RPC to grab data from a BACnet building automation system. 
[volttron github](https://github.com/VOLTTRON/volttron)

Nube-IO is also a Node-Red IoT platform that also takes advantages of Python BACnet stacks, see there git repo as well for similar tools that can also incorporate MQTT protocol like the `rubix` apps.
[nube-io github](https://github.com/NubeIO)


## Author

[linkedin](https://www.linkedin.com/in/ben-bartling-cem-cmvp-510a0961/)

## Licence

【MIT License】

Copyright 2021 Ben Bartling

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
