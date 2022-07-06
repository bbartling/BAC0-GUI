import asyncio
from aiohttp.web import Application, json_response, middleware, AppRunner,  get

import BAC0

from datetime import datetime

from models import ReadRequestModel
from models import WriteRequestModel
from models import ReleaseRequestModel
from models import ValueModel
from pydantic import ValidationError
import json

from aiohttp_basicauth import BasicAuthMiddleware
import argparse


my_parser = argparse.ArgumentParser(description='Run RestApi App as localhost or seperate device')
                       
my_parser.add_argument('-port',
                       '--port_number',
                       required=False,
                       type=int,
                       default=8080,
                       help='To change port run:$ python3 aioapp.py -port 8080')

my_parser.add_argument('-auth_user',
                       '--auth_username',
                       required=False,
                       type=str,
                       default="admin",
                       help='username for http basic authentication')

my_parser.add_argument('-auth_pass',
                       '--auth_password',
                       required=False,
                       type=str,
                       default="bacnet",
                       help='password for http basic authentication')

my_parser.add_argument('-use_basic_auth',
                       '--basic_auth',
                       required=False,
                       type=bool,
                       default=False,
                       help='Boolean to use basic auth http basic authentication')


args = my_parser.parse_args()


port_number = args.port_number
auth_username = args.auth_username
auth_password = args.auth_password
basic_auth = args.basic_auth


print('Running Rest App On Port ' + str(port_number))
print('Running Rest App http basic auth setting ' + str(basic_auth))

if basic_auth:
    print('Running Rest App http basic authentication username ' + str(auth_username))
    print('Running Rest App http basic authentication password ' + str(auth_password))



@middleware
async def _not_found_to_404(request, handler):
    try:
        return await handler(request)
    except Exception as error:
        return json_response({"key_error": f"{error}"}, status=404)



# ran in asyncio executor for blocking io
def bacnet_requester(action,req_str):
    if action == "read":
        result = bacnet.read(req_str)
    else:
        result = bacnet.write(req_str)
    return result


async def handle(request):

    global bacnet
    bacnet_req = request.match_info.get("bacnet_req", 
                                datetime.utcnow().isoformat()
                                )

    splitted = bacnet_req.split()


    if len(splitted) != 1:
        print("BACnet request is: ",bacnet_req)

        try:
            action = splitted[0]
            address = splitted[1]
            object_type = splitted[2]
            object_instance = splitted[3]

            if action == "read":

                read_vals = f'{address} {object_type} {object_instance} presentValue'

                try:
                    # validate request string with pydantic
                    testRead = ReadRequestModel(
                                            address=address,
                                            object_type=object_type,
                                            object_instance=object_instance,
                                            )

                    # if pydantic is okay, make the request to BAC0
                    read_result = await asyncio.get_running_loop().run_in_executor(None, 
                        bacnet_requester,
                        action,
                        read_vals
                        )

                    print("BACnet read for: ", read_vals," : ",read_result)
                    if isinstance(read_result, str):
                        bacnet_req = read_result
                    else:
                        bacnet_req = round(read_result,2)


                except ValidationError as error:
                    print("ReadRequestModel Error: ",error)
                    bacnet_req = f"error: {error}"
                    return json_response({bacnet_req}, status=400)


            elif action == "write":

                try:
                    value = splitted[4]
                    priority = splitted[5]

                    write_vals = f'{address} {object_type} {object_instance} presentValue {value} - {priority}'

                    # validate request string with pydantic
                    testWrite = WriteRequestModel(
                                            address=address,
                                            object_type=object_type,
                                            object_instance=object_instance,
                                            value=value,
                                            priority=priority
                                            )

                    try:
                        # validate "value" with pydantic that it is
                        # appropriate for bacnet
                        testWriteValue = ValueModel(
                                                binaryOutput="active"
                                                )

                        # if pydantic is okay, make the request to BAC0
                        write_result = await asyncio.get_running_loop().run_in_executor(None, 
                            bacnet_requester,
                            action,
                            write_vals
                            )

                        if write_result == None:
                            write_result = "write success"

                        print("BACnet write for: ", write_vals," : ",write_result)
                        bacnet_req = write_result    

                    except ValidationError as error:
                        print("TestWriteValue Error: ",error)
                        bacnet_req = f"error: {error}"
                        return json_response({bacnet_req}, status=400)

                except ValidationError as error:
                    print("WriteRequestModel Error: ",error)
                    bacnet_req = f"error: {error}"
                    return json_response({bacnet_req}, status=400)



            elif action == "release":

                try:
                    priority = splitted[4]

                    release_vals = f'{address} {object_type} {object_instance} presentValue null - {priority}'

                    # validate request string with pydantic
                    testRelease = ReleaseRequestModel(
                                            address=address,
                                            object_type=object_type,
                                            object_instance=object_instance,
                                            priority=priority
                                            )

                    # if pydantic is okay, make the request to BAC0
                    release_result = await asyncio.get_running_loop().run_in_executor(None, 
                        bacnet_requester,
                        action,
                        release_vals
                        )

                    if release_result == None:
                        release_result = "release success"

                    print("BACnet release for:", release_vals," : ",release_result)
                    bacnet_req = release_result

                except ValidationError as error:
                    print("ReleaseRequestModel Error: ",error)
                    bacnet_req = f"error: {error}"
                    return json_response({bacnet_req}, status=400)


            else:
                bacnet_req = f"error: request is not a read, write, or release"
                bacnet_req = f"error: {error}"
                return json_response({bacnet_req}, status=400)

        except Exception as error:
            bacnet_req = f"error: {error}"
            return json_response({bacnet_req}, status=400)

    return json_response(bacnet_req)


async def start_api_server():

    print("Starting Restful Api")
    loop = asyncio.get_event_loop()

    if basic_auth:
        auth = BasicAuthMiddleware(username=auth_username, password=auth_password)
        app = Application(middlewares=[_not_found_to_404,auth])

    else:
        app = Application()

    app.add_routes([get("/", handle),
                    get("/bacnet/", handle),
                    get("/bacnet/{bacnet_req}", handle)])

    #web.run_app(app)
    runner = AppRunner(app)
    await runner.setup()
    await loop.create_server(runner.server, "0.0.0.0", port_number)
    print(f"Server started on TCP http://0.0.0.0:{port_number}")



async def bacnet_worker():
    global bacnet
    print("Starting BACnet Api")
    bacnet = BAC0.lite()
    print("starting BACnet BAC0 API on UPD port 47808")
    while True:
        await asyncio.sleep(.1)


async def main():
    await(asyncio.gather(
        start_api_server(), 
        bacnet_worker()
            )
        )


if __name__ == "__main__":
    asyncio.run(main())