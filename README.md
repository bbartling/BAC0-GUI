# Flask restful bacnet

This is a RESTful interface to retrieve data from BACnet building automation systems. The idea is to run this Flask web app on the same LAN as the building automation system along side NODE-RED as localhost to take advantage of Python BACnet stacks. The Flask App accepts JSON payloads and hands off the BACnet features to BAC0 (runs on a UDP port 47808) which is a Python BACnet App developed by Christian Tremblay.

See BAC0 documention for what is going under the hood of the Flask App:
https://bac0.readthedocs.io/en/latest/


## Overview

- .gitignore
- flaskapp.py
- README.md
- requirements.txt
- runtime.txt


## Requirements

See requirements.txt.

## Deployment for non localhost or localhost Flask App
See optional argument below for a `localhost` deployment

## Installation & Usage

```bash
$ git clone https://github.com/bbartling/flask-restul-bacnet.git
# Or using downloaded zip file 
$ unzip flask-restul-bacnet.zip

# change the directory
$ cd flask-restul-bacnet

# install packages
$ pip install -r requirements.txt

# start the app
# by default runs on host IP address of 0.0.0.0
# to access the restAPI from a different device
$ python flaskapp.py
```

If you want to run the Flask App as localhost ONLY use this below when you run the Python file, as localhost the rest API will not be accessible from other computers on the LAN only localhost:

```
# start the app to run as localhost
# to access restAPI from same machine
$ python flaskapp.py -ip localhost
```


The Flask App runs on port 5000, the BACnet features (BAC0) runs on UDP port 47808.

On startup BAC0 performs a BACnet "whois" where the screenshot below shows 2 BACnet devices that replied. Device 192.168.0.190 is an IP based BACnet device and device 201201 (BACnet instance ID) on MSTP network 12345 with hardware address 2 shown. This App supports both MSTP devices and IP based BACnet controllers.

*Please advise on large BACnet sites this portion of the code could be commented out to prevent unwanted BACnet traffice or network congestion. Like a game of ping pong the Flask app only supports one argument(URL endpoint) at a time to as shown in the insomnia screenshots. The BACnet device information to be retreived or written needs to be entered in the body of the HTTP GET request as JSON payload. One thing to note is Flask as well as the BACnet stacks running under the hood are all synchronous non-thread safe Python libraries.

![Start Up](/images/startup.PNG)


## HTTP GET Requests for singe BACnet point
-json payload in body of GET request structure as shown in the screenshots below

/bacnet/read/single
![read](/images/read.PNG)

/bacnet/write/single
![write](/images/write.PNG)

/bacnet/release/single
![release](/images/release.PNG)


## HTTP GET Requests for multiple BACnet point
-json payload in body of GET request structure as shown in the screenshots below

/bacnet/read/multiple
![read](/images/read_mult.PNG)

/bacnet/write/multiple
![write](/images/write_mult.PNG)

/bacnet/release/multiple
![release](/images/release_mult.PNG)

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
