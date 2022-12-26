import BAC0,time,json 
from flask import Flask, request, jsonify
import flask
import logging
import argparse
from models import ReadRequestModel
from models import WriteRequestModel
from models import ReleaseRequestModel
from models import ValueModel
	
from flask_pydantic import validate


#logging.basicConfig(filename='_log_flask.log', level=logging.WARNING)



#STATIC_BACNET_IP = '192.168.0.103/24'
#bacnet = BAC0.lite(IP=STATIC_BACNET_IP)
bacnet = BAC0.lite()
app = Flask(__name__)




@app.route('/bacnet/read', methods=['POST'])
@validate()
def reader(body: ReadRequestModel):

    json_data = flask.request.json                 
    try:
        read_str = f"{json_data['address']} {json_data['object_type']} \
            {json_data['object_instance']} presentValue"
            
        print("Excecuting read str:", read_str)
        read_result = bacnet.read(read_str)

        if type(float(read_result)):
            read_result = round(read_result,2)
        return {"status" : "success", "pv":read_result}
    
    except Exception as e:
        return {"status" : "BACnet Error", "pv":e}, 403
    

@app.route('/bacnet/write', methods=['POST'])
@validate()
def writer(body: WriteRequestModel):

    json_data = flask.request.json                 
    try:
        write_str = f"{json_data['address']} {json_data['object_type']} {json_data['object_instance']} presentValue {json_data['value']} - {json_data['priority']}"
            
        print("Excecuting write str:", write_str)
        bacnet.write(write_str)

        return {"status" : "success", "point": write_str}
    
    except Exception as e:
        return {"status" : "BACnet Write Error", 
                "point": write_str - e}, 403


@app.route('/bacnet/release', methods=['POST'])
@validate()
def releaser(body: ReleaseRequestModel):

    json_data = flask.request.json              
    try:
        release_str = f"{json_data['address']} {json_data['object_type']} {json_data['object_instance']} presentValue null - {json_data['priority']}"
            
        print("Excecuting release str:", release_str)
        bacnet.write(release_str)

        return {"status" : "success", "point": release_str}
    
    except Exception as e:
        return {"status" : "BACnet Release Error", 
                "point": release_str - e}, 403


if __name__ == '__main__':
    print("Starting main loop")

    my_parser = argparse.ArgumentParser(description='Run Flask App as localhost or seperate device')
    my_parser.add_argument('-ip',
                           '--host_address',
                           required=False,
                           type=str,
                           default='0.0.0.0',
                           help='Default is to run app on a seperate device. To run as localhost try: python3 flaskapp.py -ip localhost')
    args = my_parser.parse_args()

    host_address = args.host_address
    print('Host IP Address Config for the Flask App Is ' + host_address)

    app.run(debug=False,port=5000,host=host_address,use_reloader=False)


