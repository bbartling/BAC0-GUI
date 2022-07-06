# bacnet-restapi

This is a RESTful interface made with Python web stacks and Python BACnet stacks to retrieve data from BACnet building automation systems (BAS) with typical industry standard BACnet read, writes, and release commands on BACnet `presentValue` point attributes. The idea is to run this app along side the BAS on a buildings LAN (NOT a cloud environment) and receive data back in JSON format.


## Overview

- .gitignore
- main.py
- models.py
- README.md
- requirements.txt
- runtime.txt


## Requirements

See requirements.txt.


## Installation & Usage With Node Red

Tested on Ubuntu 20.04 LTS and should also work in Windows 10 as well.

On Linux this app is started via SSH into the linux instance and tmux is used to keep the script alive after disconnecting from the SSH session. [tmux Repo Link](https://github.com/tmux/tmux/wiki)

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
$ python3 main.py
```

* Note web app runs on port 8080. A `GET` request on the base URL will return server time in UTC ISO format. Examples below the base URL is `127.0.0.1` but just replace this with whatever the IP address is of your machine that you are running this app on.


# Example `GET` HTTP requests to the restapi app for a "read" of BACnet present value:
* [See BAC0 syntax](https://bac0.readthedocs.io/en/latest/read.html#read-examples) for read requests to understand what runs under the hood in the web app
* Note, for MSTP network devices use syntax like "12345:2" to represent BACnet hardware address 2 on MSTP network 12345

 In the browser this will look like: `http://127.0.0.1:8080/read 10.200.200.27 binaryOutput 3`

This would be read the BACnet present value of binary output 3 on device 10.200.200.27 and return JSON `"active"` or `"inactive"` because its a binary output or Boolean type of point. Boolean objects are strings in BAC0 as "active" or "inactive" where in this example the cooling compressors on the rooftop HVAC have a status of either "active" or "inactive."


# Example `GET` HTTP requests to the restapi app for a "write" of BACnet present value:
* [See BAC0 syntax](https://bac0.readthedocs.io/en/latest/read.html#write-to-property) for write requests but note this web app only permits `presentValue` operations

In the browser this will look like: `http://127.0.0.1:8080/write 10.200.200.27 binaryOutput 3 active 12`

This would be write the BACnet present value of binary output 3 on device 10.200.200.27 to "active" on BACnet prority 12.


# Example `GET` HTTP requests to the restapi app for a "release" of BACnet present value:
* This uses the BAC0 write syntax but minus a value to "write," for example in the browser:

In the browser this will look like: `http://127.0.0.1:8080/release 10.200.200.27 binaryOutput 3 12`

This would be release the BACnet present value of binary output 3 on device 10.200.200.27 on BACnet priority 12. Under the hood in the web app `null` in BAC0 represent release but incorporating a `null` value is handled by the web app.


## Note about Rasp pi Buster:
If running python 3.7 or default rasp pi Buster image. This has been tested on a rasp pi Buster image with upgrading Python to 3.9 using this tutorial:
https://itheo.tech/ultimate-python-installation-on-a-raspberry-pi-ubuntu-script



## Auto Scan BACnet network
Check out [BACpypes-snapshot](https://github.com/JoelBender/bacpypes-snapshot) which is a cool tool to see what the BACnet network has for devices and BACnet point attributes for all devices.


## Issues and comments
Please submit git issues to improve app as well as bugs found during testing. 


## Author
[linkedin](https://www.linkedin.com/in/ben-bartling-cem-cmvp-510a0961/)

## Licence
【MIT License】

Copyright 2022 Ben Bartling

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
