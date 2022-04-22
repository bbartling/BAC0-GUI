# bacnet-restapi

This is a RESTful interface made with Python web stacks and Python BACnet stacks to retrieve data from BACnet building automation systems (BAS) with typical industry standard BACnet read, writes, and release commands. The idea is to run this app along side the BAS on a buildings LAN which is NOT a cloud environment.


## Overview

- .gitignore
- flaskapp.py
- README.md
- requirements.txt
- runtime.txt


## Requirements

See requirements.txt.


## Installation & Usage With Node Red

Tested on Ubuntu 20.04 LTS with running the Python web app along side Node Red. This app can also run on a seperate device like a rasp pi but see caveats below if using a `Buster` image that runs Python 3.7.

The app is started via SSH into the linux instance and tmux is used to keep the script alive after disconnecting from the SSH session. [tmux Repo Link](https://github.com/tmux/tmux/wiki)



# Start Python Web App 
```
# clone git repo and change directory into it
$ git clone https://github.com/bbartling/bacnet-restapi
$ cd bacnet-restapi/

# make sure TMUX is started or some other method to keep the script alive after the SSH session is ended

# OPTIONAL STEP 1: create virtual enviornment to install Python packages
$ python3 -m venv env

# OPTIONAL STEP 2: activate virtual enviornment
$ source env/bin/activate

# install packages with pip
$ pip3 install -r requirements.txt

# start the restapi web app
$ python3 aioapp.py
```

# Args Note when starting the web app for network port and HTTP basic authentication.

`-port` is an optional arguments for command prompt when starting the Python app. The default port is 5000 is not port is specified. 

`-auth_user` and `-auth_pass` are optional arguments for command prompt when starting the Python app for HTTP basic authentication. The default username is `admin` and default password is `bacnet`. 

```
# example to run the web app on port `8080` with `hulk` for username and `smash` for the HTTP basic authentication. 

$ python3 aioapp.py -port 8080 -auth_user hulk -auth_pass -smash

# See the flask_version of this repo for an older version of this app that uses no authentication if that is desired.

```

# Swagger 2.0 for OpenAPI rest endpoints:
After Python web app starts go to the device URL, the link is for localhost browsing: [http://127.0.0.1:8080/oas](http://127.0.0.1:8080/oas) to bring up a page that looks like this below:
![Swagger1](/images/swagger1.PNG)

BACnet Read Single:
```
{
  "address": "string",
  "object_type": "string",
  "object_instance": "string"
}
```


# Example `GET` HTTP requests to the restapi app with JSON in body for read single:

* Note, "12345:2" represent BACnet hardware address 2 on MSTP network 12345

```
{
	"address":"12345:2",
	"object_type":"analogInput",
	"object_instance":"2"
}
```

In node red debug you should see:

![debug_read_single](/images/debug_read_single.PNG)

BACnet Read Multiple:
```
{
  "devices": {
    "additionalProp1": {
      "address": "string",
      "object_type": "string",
      "object_instance": "string"
    },
    "additionalProp2": {
      "address": "string",
      "object_type": "string",
      "object_instance": "string"
    },
    "additionalProp3": {
      "address": "string",
      "object_type": "string",
      "object_instance": "string"
    }
  }
}
```

# Example `GET` HTTP requests to the restapi app with JSON in body for a read multiple:
* Note where below `"devices"` can be limiteless but example only shows boiler, cooling plant, AHU, and hot water valve which are all seperate BACnet devices in the BAS system. Read, write, release multiple can be all from the same device or seperate devices.

```
{"devices":{
    "boiler_return_temp":{
    "address":"12345:2",
    "object_type":"analogInput",
    "object_instance":"2"
    },
    "cooling_plant_leaving_temp":{
    "address":"192.168.0.100",
    "object_type":"multistateValue",
    "object_instance":"225"
    },
    "air_handler_1_fan_status":{
    "address":"192.168.0.101",
    "object_type":"binaryInput",
    "object_instance":"12"
    },
    "air_handler_2_fan_command":{
    "address":"12345:5",
    "object_type":"binaryOutput",
    "object_instance":"1"
    },
    "heater_water_valve_cmd":{
    "address":"12345:2",
    "object_type":"analogOutput",
    "object_instance":"7"
    }
}}
```

returned JSON of sensor readings BACnet present values:

```
{
  "status": "read_success",
  "data": {
    "boiler_return_temp": {
      "pv": 167.01
    },
    "cooling_plant_leaving_temp": {
      "pv": 44.31
    },
    "air_handler_1_fan_status": {
      "pv": False
    },
    "air_handler_2_fan_command": {
      "pv": active
    },
    "heater_water_valve_cmd": {
      "pv": 87.39
    }
  }
}
```

Errors would come through with a string `error` if the point doesnt exist in the BACnet device or if something is actually happening on the BACnet side preventing a proper read, write, or release.
![debug_read_mult](/images/debug_read_mult.PNG)


See swagger definition for writes and release that require extra parameters specifying priority and value to write.



# Note about Rasp pi Buster:
Use the [flask_version](https://github.com/bbartling/bacnet-restapi/tree/main/flask_version) if running python 3.7 or default rasp pi Buster image. This has been tested on a rasp pi Buster image with upgrading Python to 3.9 using this tutorial:
https://itheo.tech/ultimate-python-installation-on-a-raspberry-pi-ubuntu-script



## Auto Scan BACnet network
See the [scanning_scripts](https://github.com/bbartling/bacnet-restapi/tree/main/scanning_scripts) directory of this repo for an experimental process of auto scanning the BACnet to compile results into a CSV file.


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
