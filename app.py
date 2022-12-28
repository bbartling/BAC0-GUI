import BAC0

import argparse,logging,time
from models import ReadRequestModel
from models import WriteRequestModel
from models import ReleaseRequestModel

from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path
from dataclasses import dataclass
from flask_pydantic import validate


#logging.basicConfig(filename='_log_flask.log', level=logging.WARNING)

#STATIC_BACNET_IP = '192.168.0.103/24'
#bacnet = BAC0.lite(IP=STATIC_BACNET_IP)
bacnet = BAC0.lite()

BASE_DIR = Path(__file__).parent
print(BASE_DIR)
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(BASE_DIR.joinpath('db.sqlite'))
print(SQLALCHEMY_DATABASE_URI)


db = SQLAlchemy()

def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    print('Setup DB Success!')
    
    
def db_drop_and_create_all(app):
    with app.app_context():
        db.drop_all()
        db.create_all()
        print('DB drop all and create all Success!')
        '''
        example1 = BacnetOverrides(title='12345:2 analogValue 302 presentValue 55 - 11')
        example2 = BacnetOverrides(title='12345:2 analogValue 302 presentValue 55 - 11')
        db.session.add(example1)
        db.session.add(example2)
        db.session.commit()
        BacnetOverridess = BacnetOverrides.query.all()
        print('BacnetOverridess: ',BacnetOverridess)
        print('example1.id: ',example1.id)
        print('example2.id: ',example2.id)
        print(BacnetOverrides.query.all())
        '''
        

@dataclass
class BacnetOverrides(db.Model):
    
    id: int
    title: str
    date: datetime
    released: bool
    
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(140))
    date = db.Column(db.DateTime(),default=datetime.now())
    released = db.Column(db.Boolean(),default=False)
    
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        
    def __repr__(self):
        return f'<BacnetOverrides id: {self.id} - {self.title}'


def make_flask_app(USE_DASHBOARD):
    print('DASHBOARD ENABLED IS: ' + str(USE_DASHBOARD))

    app = Flask(__name__)

    setup_db(app)
    db_drop_and_create_all(app)

    if USE_DASHBOARD:
        @app.route('/')
        def index():
            BacnetOverridess = BacnetOverrides.query.all()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify(BacnetOverridess)
            return render_template('index.html')
    else:
        @app.route('/')
        def index():
            return jsonify({'server_time': str(time.ctime())})


    def add_override_to_db(add_override_str):
        print('INPUTING NEW OVERRIDE INTO DB',add_override_str)
        do = BacnetOverrides(title=add_override_str)
        db.session.add(do)
        db.session.commit()
        print('DB COMMIT SUCCESS!')
            

    def delete_BacnetOverrides(remove_override_str,override_id):
        print('REMOVING OVERRIDE FROM DB',remove_override_str)
        do = BacnetOverrides.query.filter_by(id=override_id).first()
        db.session.delete(do)
        db.session.commit()
        print('DB COMMIT SUCCESS!')


    @app.route('/bacnet/read/', methods=['POST'])
    @validate() # flask pydantic
    def reader(body: ReadRequestModel):

        try:
            r = request.json 
            read_str = f"{r['address']} {r['object_type']} {r['object_instance']} presentValue"
            print("Excecuting read str:", read_str)
            read_result = bacnet.read(read_str)
            if type(float(read_result)):
                read_result = round(read_result,2)
            return jsonify({"status" : "success", "pv":read_result})
        except Exception as e:
            return jsonify({"status" : "error", "pv": e}), 500
        

    @app.route('/bacnet/write/', methods=['POST'])
    @validate() # flask pydantic
    def writer(body: WriteRequestModel):
        
        try:
            r = request.json 
            write_str = f"{r['address']} {r['object_type']} {r['object_instance']} presentValue {r['value']} - {r['priority']}"
            print("Excecuting write str:", write_str)
            bacnet.write(write_str)
            add_override_to_db(write_str) # add to sqlite db for dashboard
            return jsonify({"status" : "success", "point": write_str})
        except Exception as e:
            return jsonify({"status" : "error", 
                    "point": e}), 500


    @app.route('/bacnet/release/', methods=['POST'])
    @validate() # flask pydantic
    def releaser(body: ReleaseRequestModel):
        
        try:
            r = request.json 
            print("release r: ",r)
            
            release_str = f"{r['address']} {r['object_type']} {r['object_instance']} presentValue null - {r['priority']}"
            print("Excecuting release str:", release_str)
            bacnet.write(release_str)
            delete_BacnetOverrides(release_str,r['id']) # remove from sqlite db for dashboard
            return jsonify({"status" : "success", "point": release_str})
        except Exception as e:
            return jsonify({"status" : "error", 
                    "point": e}), 500
            
            
    return app


if __name__ == '__main__':
    print("Starting main loop")
    parser = argparse.ArgumentParser(add_help=False)
    args = parser.add_argument_group('Options')
    args.add_argument('-port',
                        '--port_number',
                        required=False,
                        type=int,
                        default=5000,
                        help='Port number to run web app')    

    args.add_argument('--use-localhost', default=False, action='store_true')
    args.add_argument('--no-localhost', dest='use-localhost', action='store_false')

    args.add_argument('--use-dashboard', default=False, action='store_true')
    args.add_argument('--no-dashboard', dest='use-dashboard', action='store_false')
    
    args = parser.parse_args()
    print('args.use_dashboard: ',args.use_dashboard)
    
    if args.use_localhost:
        host_address='localhost'
        print('Running app on localhost only! App and rest endpoints will not be accessable from outside this device!')
    else:
        host_address='0.0.0.0'
        
    print('Host Address Config Is: ' + host_address)
    app = make_flask_app(args.use_dashboard)
    app.run(debug=False,host=host_address,port=args.port_number,use_reloader=False)