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

The demo will utilize [Node Red Generator](https://github.com/node-red/node-red-nodegen/wiki)


```
# tmux window pane 1


# Install node red generator with npm
$ npm install -g node-red-nodegen

# Git clone the python web app repo
$ git clone https://github.com/bbartling/bacnet-restapi.git

# Change the directory
$ cd bacnet-restapi/swagger_json

# Auto generate requests with node red gen
$ sudo node-red-nodegen testing.json

# In the bacnet-restapi/swagger_json directory
# Change directory to the generated node's directory
$ node-red-contrib-aiohttp-pydantic-application

# Prepare the symbolic link
$ sudo npm link

# change directory
$ cd ~/.node-red

# Change current directory to Node-RED home directory (Typically, Node-RED home directory is ".node-red" under the home directory)
$ npm link node-red-contrib-aiohttp-pydantic-application

# Start Node-RED
$ node-red
```


# Start Python Web App
```
# bash tmux session 2
# run the BACnet restful app

$ cd bacnet-restapi/

# create virtual enviornment to install Python packages
$ python3 -m venv env

# activate virtual enviornment
$ source env/bin/activate

# install packages with pip
$ pip3 install -r requirements.txt

# start the restapi web app
$ python3 aioapp.py
```

# Args Note when starting the Python app

```
# -ip and -port is optional arguments, the default port is 5000.
# The default web IP is 0.0.0.0.
# You can specify localhost which will lockout the web app api
# from external HTTP requests from outside the PC.
# If running on a rasp pi or seperate device from the Node Red
# instance just use default or no args for specifying the web app
# IP address. 

# example to run the web app on local host on port 8080
$ python3 aioapp.py -ip localhost -port 8080

```


# Node Red Function Block Builder

If the function block builder compiles correctly you should see a block that looks like this:

![functionBlock1](/images/functionBlock1.PNG)

Drag it out on the pallete, open it up to edit:

![functionBlock2](/images/functionBlock2.PNG)

I'm running my Python app on:

![functionBlock3](/images/functionBlock3.PNG)

Wire in an Inject block and set header for json
`{"content-type":"application/json"}`

As well as the `msg.payload` is your json request for the BACnet instances to read.

![functionBlock4](/images/functionBlock4.PNG)


# [Swagger](https://swagger.io/resources/open-api/) for OpenAPI rest endpoints:
After app starts go to the device URL: [http://127.0.0.1:8080/oas](http://127.0.0.1:8080/oas) to bring up a page that looks like this below:
![Swagger1](/images/swagger1.PNG)


# Example `GET` HTTP requests to the restapi app with JSON in body:

BACnet Read Single:
`192.168.0.105:5000/bacnet/read/single`

```
{
	"address":"12345:2",
	"object_type":"analogInput",
	"object_instance":"2"
}
```

BACnet Read Multiple:
`192.168.0.105:5000/bacnet/read/multiple` where below `"devices"` can be limiteless but example only shows boiler, cooling plant, AHU, and hot water valve which are all seperate BACnet devices in the BAS system. Read, write, release multiple can be all from the same device or seperate devices.

```
{"devices":{
    "boiler_return_temp":{
    "address":"12345:2",
    "object_type":"analogInput",
    "object_instance":"2"
    },
    "cooling_plant_leaving_temp":{
    "address":"12345:3",
    "object_type":"multistateValue",
    "object_instance":"225"
    },
    "air_handler_1_fan_status":{
    "address":"12345:4",
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
      "pv": True
    },
    "heater_water_valve_cmd": {
      "pv": 87.39
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
