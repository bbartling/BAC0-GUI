import BAC0,time,json 
from flask import Flask, request, jsonify
import flask
import logging
import argparse

logging.basicConfig(filename='_log_flask.log', level=logging.WARNING)



#STATIC_BACNET_IP = '192.168.0.103/24'
#bacnet = BAC0.lite(IP=STATIC_BACNET_IP)

bacnet = BAC0.lite()


#start flask app
app = Flask(__name__)


#READ
@app.route('/bacnet/read/single', methods=['GET'])
def reader():

    try:
        json_data = flask.request.json
        address = json_data["address"]
        object_type = json_data["object_type"]
        object_instance = json_data["object_instance"]

        read_vals = f'{address} {object_type} {object_instance} presentValue'
        print("Excecuting read_vals statement:", read_vals)
        read_result = bacnet.read(read_vals)
        read_result_round = round(read_result,2)
        response_obj = { 'status' : 'success', 'pv' : read_result_round }
        
    except Exception as error:
        logging.error("Error trying BACnet Read {}".format(error))
        info = str(error)
        print(error)
        response_obj = { 'status' : 'fail', 'pv' : info }
        return jsonify(response_obj), 500

    return jsonify(response_obj)


#WRITE
@app.route('/bacnet/write/single', methods=['GET'])
def writer():

    try:
        json_data = flask.request.json
        address = json_data["address"]
        object_type = json_data["object_type"]
        object_instance = json_data["object_instance"]
        value = json_data["value"]
        priority = json_data["priority"]
    
        write_vals = f'{address} {object_type} {object_instance} presentValue {value} - {priority}'
        print("Excecuting write_vals statement:", write_vals)
        bacnet.write(write_vals)
        info = f'BACnet point written to device'
        response_obj = { 'status' : 'success', 'info' : info }
        
    except Exception as error:
        logging.error("Error trying BACnet Write {}".format(error))
        info = str(error)
        print(error)
        response_obj = { 'status' : 'fail', 'info' : info }
        return jsonify(response_obj), 500

    return jsonify(response_obj)


#RELEASE
@app.route('/bacnet/release/single', methods=['GET'])
def releaser():

    try:
        json_data = flask.request.json
        address = json_data["address"]
        object_type = json_data["object_type"]
        object_instance = json_data["object_instance"]
        priority = json_data["priority"]
    
        write_vals = f'{address} {object_type} {object_instance} presentValue null - {priority}'
        print("Excecuting write_vals statement:", write_vals)
        bacnet.write(write_vals)
        info = f'BACnet point release to device'
        response_obj = { 'status' : 'success', 'info' : info }
        
    except Exception as error:
        logging.error("Error trying BACnet Release {}".format(error))
        info = str(error)
        print(error)
        response_obj = { 'status' : 'fail', 'info' : info }
        return jsonify(response_obj), 500

    return jsonify(response_obj)


#READ MULTIPLE
@app.route('/bacnet/read/multiple', methods=['GET'])
def reader_mult():

    try:
        json_data = flask.request.json
        device_mapping = {}

        try:
            for device,values in json_data.items():
                address = values["address"]
                object_type = values["object_type"]
                object_instance = values["object_instance"]
                read_vals = f'{address} {object_type} {object_instance} presentValue'
                print("Excecuting read multiple statement:", read_vals)
                read_result = bacnet.read(read_vals)
                read_result_round = round(read_result,2)
                device_mapping[device] = {'pv':read_result_round}

        except:
            device_mapping[device] = {'pv' : 'error'}
 
        response_obj = { 'status' : 'success', 'data' : device_mapping }
        
    except Exception as error:
        logging.error("Error trying BACnet Read Multiple {}".format(error))
        info = str(error)
        print(error)
        response_obj = { 'status' : 'fail', 'read_info' : info }
        return jsonify(response_obj), 500

    return jsonify(response_obj)



#WRITE MULTIPLE
@app.route('/bacnet/write/multiple', methods=['GET'])
def writer_mult():

    try:
        json_data = flask.request.json
        device_mapping = {}

        try:
            for device,values in json_data.items():
                address = values["address"]
                object_type = values["object_type"]
                object_instance = values["object_instance"]
                value = values["value"]
                priority = values["priority"]
            
                write_vals = f'{address} {object_type} {object_instance} presentValue {value} - {priority}'
                print("Excecuting Write Mult Statement:", write_vals)
                bacnet.write(write_vals)
                device_mapping[device] = {object_type + ' ' + object_instance : value }

        except:
            device_mapping[device] = {object_type + ' ' + object_instance : 'error' }

        response_obj = { 'status' : 'success', 'info' : device_mapping }
        
    except Exception as error:
        logging.error("Error trying BACnet Write Multiple {}".format(error))
        info = str(error)
        print(error)
        response_obj = { 'status' : 'fail', 'write_info' : info }
        return jsonify(response_obj), 500

    return jsonify(response_obj)


#RELEASE MULTIPLE
@app.route('/bacnet/release/multiple', methods=['GET'])
def releaser_mult():

    try:
        json_data = flask.request.json
        print(json_data)
        device_mapping = {}

        try:
            for device,values in json_data.items():
                print(device)
                print(values)
                address = values["address"]
                object_type = values["object_type"]
                object_instance = values["object_instance"]
                priority = values["priority"]
            
                write_vals = f'{address} {object_type} {object_instance} presentValue null - {priority}'
                print("Excecuting Release Mult Statement:", write_vals)
                bacnet.write(write_vals)
                device_mapping[device] = {object_type + ' ' + object_instance : 'success'}

        except:
            device_mapping[device] = {object_type + ' ' + object_instance : 'error'}

        response_obj = { 'status' : 'success', 'release_info' : device_mapping }
        
    except Exception as error:
        logging.error("Error trying BACnet Release Multiple {}".format(error))
        info = str(error)
        print(error)
        response_obj = { 'status' : 'fail', 'info' : info }
        return jsonify(response_obj), 500

    return jsonify(response_obj)


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


