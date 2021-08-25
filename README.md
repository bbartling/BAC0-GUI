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


## Requirement

See requirements.txt.

## deployment for non localhost or localhost Flask App
If you deploy this app on a different machine, like a rasp pi use flaskapp.py
For localhost deployment on the same machine as node-red use flaskapp_localhost.py

## Installation & Usage

```bash
$ git clone https://github.com/bbartling/flask-restul-bacnet.git
# Or using downloaded zip file 
$ unzip flask-restul-bacnet.zip

# change the directory
$ cd flask-restul-bacnet
# install packages
$ pip install -r requirements.txt
# start the server
$ python flaskapp.py
```

Flask App Runs on:

http://127.0.0.1:5000/ or as localhost with `flaskapp_localhost.py`

BAC0 runs on UDP port 47808.

On startup BAC0 performs a BACnet "whois" where the screenshot below shows 2 BACnet devices that replied. Device 192.168.0.190 is an IP based BACnet device and device 201201 (BACnet instance ID) on MSTP network 12345 with hardware address 2 shown. This App supports both MSTP devices and IP based BACnet controllers.

*Please advise on large BACnet sites this portion of the code could be commented out to prevent unwanted BACnet traffice or network congestion.

![Start Up](/images/startup.PNG)


## HTTP GET Requests

App Supports 3 GET requests to read, write, or release BACnet. Like a game of ping pong the Flask app at the moment only supports one BACnet point at a time to as shown in the insomnia screenshots below the BACnet device information needs to be entered in the body of the GET request. One thing to note is Flask as well as the BACnet stacks running under the hood are all synchronous non-thread safe Python libraries.

/bacnet/read/single
![read](/images/read.PNG)

/bacnet/write/single
![write](/images/write.PNG)

/bacnet/release/single
![release](/images/release.PNG)


## FUTURE development 
Include multiple BACnet point read, write, and releases stay tuned to the repo. Please submit git issues to improve app as well as bugs found during testing.


## Author

[linkedin](https://www.linkedin.com/in/ben-bartling-cem-cmvp-510a0961/)

## Licence

【MIT License】

Copyright 2021 Ben Bartling

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
