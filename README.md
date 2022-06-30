# bacnet-restapi

This is a RESTful interface made with Python web stacks and Python BACnet stacks to retrieve data from BACnet building automation systems (BAS) with typical industry standard BACnet read, writes, and release commands on BACnet `presentValue` point attributes. The idea is to run this app along side the BAS on a buildings LAN which is NOT a cloud environment.


## Overview

- .gitignore
- main.py
- models.py
- bacnet_actions.py
- views.py
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

## Args Note when starting the Python app

`-ip` and `-port` are optional arguments for command prompt when starting the Python app. The default port is 5000. The default web IP is 0.0.0.0. You can specify localhost which will lockout the web app api from external HTTP requests from outside the PC. If running on a rasp pi or seperate device from the Node Red instance just use default or no args for specifying the web app IP address. 

```
# example to run the web app on local host on port 8080
$ python3 main.py -ip localhost -port 8080

```

`-use_auth`,  `-auth_user`, and `-auth_pass` are optional arguments for Basic Authentication on the all rest endpoints of the BACnet rest API app. Below would be an example for how to start the APP with authentication and `admin` as the username and `bacnet` as the password. By default authentication is not required.

```
# example to run the web app on local host on port 8080
$ python3 main.py -use_auth True -auth_user admin -auth_pass bacnet

```


## Swagger 2.0 for OpenAPI rest endpoints:
After Python web app starts go to the device URL, the link in this example is for localhost browsing: [http://127.0.0.1:5000/oas](http://127.0.0.1:5000/oas) but replace `127.0.0.1` with the IP address of your device running this app:
![Swagger1](/images/swagger1.PNG)



# Example `GET` HTTP requests to the restapi app with JSON in body for a "read" of BACnet present value on a single point:

* Note, for MSTP network devices use sntax like "12345:2" to represent BACnet hardware address 2 on MSTP network 12345
* http://127.0.0.1:5000/bacnet/read/single

```
{
  "address":"10.200.200.27",
  "object_type":"binaryOutput",
  "object_instance":"3"
}
```


# Example `GET` HTTP requests to the restapi app with JSON in body for a "read" of BACnet present value on multiple points:

* http://127.0.0.1:5000/bacnet/read/multiple

This example below is reading all cooling compressor status:
```
{
"read": 
  [    
    {
      "address": "10.200.200.27",
      "object_type": "binaryOutput",
      "object_instance": "3"
      },
        {
        "address": "10.200.200.27",
        "object_type": "binaryOutput",
        "object_instance": "4"
      },
      {
        "address": "10.200.200.27",
        "object_type": "binaryOutput",
        "object_instance": "5"
      },
      {
        "address": "10.200.200.27",
        "object_type": "binaryOutput",
        "object_instance": "6"
      }
  ]
}
```

This will return a list where binary output BACnet objects come through in strings as "active" or "inactive":

```
[
  "active",
  "active",
  "inactive",
  "inactive"
]
```


# Example `GET` HTTP requests to the restapi app with JSON in body for a "write" of BACnet present value on a single point:

* Note, same as above on the "read" but with additional params for "value" and BACnet "priority"
* http://127.0.0.1:5000/bacnet/write/single

```

{
  "address": "10.200.200.27",
  "object_type": "binaryOutput",
  "object_instance": "3",
  "value" : "active",
  "priority" : "12"
}
```

# Example `GET` HTTP requests to the restapi app with JSON in body for a "write" BACnet present value on multiple points:

* http://127.0.0.1:5000/bacnet/write/multiple
This example below is writing values all cooling compressor status:

```
{
"write": 
  [    
    {
        "address": "10.200.200.27",
        "object_type": "binaryOutput",
        "object_instance": "3",
        "value" : "active",
        "priority" : "12"
      },
        {
        "address": "10.200.200.27",
        "object_type": "binaryOutput",
        "object_instance": "4",
        "value" : "active",
        "priority" : "12"
      },
      {
        "address": "10.200.200.27",
        "object_type": "binaryOutput",
        "object_instance": "5",
        "value" : "active",
        "priority" : "12"
      },
      {
        "address": "10.200.200.27",
        "object_type": "binaryOutput",
        "object_instance": "6",
        "value" : "active",
        "priority" : "12"
      }
  ]
}

```

This will return a list of the status for the BACnet writes made to the cooling compressors:

```
[
  "success",
  "success",
  "success",
  "success"
]
```


# Example `GET` HTTP requests to the restapi app with JSON in body for a "release" of BACnet present value on a single point:

* Note, same as above on the "write" but without the param for "value"
* http://127.0.0.1:5000/bacnet/release/single

```

{
  "address": "10.200.200.27",
  "object_type": "binaryOutput",
  "object_instance": "3",
  "priority" : "12"
}
```

# Example `GET` HTTP requests to the restapi app with JSON in body for a "release" BACnet present value on multiple points:

* http://127.0.0.1:5000/bacnet/release/multiple
This example below is releasing all cooling compressor BACnet writes on priority 12:

```
{
"release": 
  [    
    {
        "address": "10.200.200.27",
        "object_type": "binaryOutput",
        "object_instance": "3",
        "priority" : "12"
      },
        {
        "address": "10.200.200.27",
        "object_type": "binaryOutput",
        "object_instance": "4",
        "priority" : "12"
      },
      {
        "address": "10.200.200.27",
        "object_type": "binaryOutput",
        "object_instance": "5",
        "priority" : "12"
      },
      {
        "address": "10.200.200.27",
        "object_type": "binaryOutput",
        "object_instance": "6",
        "priority" : "12"
      }
  ]
}


```

This will return a list of the status for the BACnet releases made to the cooling compressors:

```
[
  "success",
  "success",
  "success",
  "success"
]
```



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
