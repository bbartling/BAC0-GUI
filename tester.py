import asyncio
from aiohttp import web
import BAC0
from datetime import datetime



# read 10.200.200.27 binaryOutput 3
# write 10.200.200.27 binaryOutput 3 active 12
# release 10.200.200.27 binaryOutput 3 12


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


            elif action == "write":
                value = splitted[4]
                priority = splitted[5]

                write_vals = f'{address} {object_type} {object_instance} presentValue {value} - {priority}'
                write_result = await asyncio.get_running_loop().run_in_executor(None, 
                    bacnet_requester,
                    action,
                    write_vals
                    )

                if write_result == None:
                    write_result = "write success"

                print("BACnet write for: ", write_vals," : ",write_result)
                bacnet_req = write_result         

            elif action == "release":
                priority = splitted[4]

                release_vals = f'{address} {object_type} {object_instance} presentValue null - {priority}'
                release_result = await asyncio.get_running_loop().run_in_executor(None, 
                    bacnet_requester,
                    action,
                    release_vals
                    )

                if release_result == None:
                    release_result = "release success"

                print("BACnet release for:", release_vals," : ",release_result)
                bacnet_req = release_result

            else:
                bacnet_req = f"error: request does not start with read, write, or release"

        except Exception as error:
            bacnet_req = f"error: {error}"

    return web.json_response(bacnet_req)


async def start_api_server():
    print("starting api")
    loop = asyncio.get_event_loop()
    app = web.Application()
    app.add_routes([web.get("/", handle),
                    web.get("/{bacnet_req}", handle)])


    #web.run_app(app)
    runner = web.AppRunner(app)
    await runner.setup()
    await loop.create_server(runner.server, "0.0.0.0", 8080)
    print("Server started at http://0.0.0.0:8080...")



async def bacnet_worker():
    global bacnet
    print("starting bacnet worker")
    bacnet = BAC0.lite()
    while True:
        await asyncio.sleep(.01)


async def main():
    await(asyncio.gather(
        start_api_server(), 
        bacnet_worker()
            )
        )


if __name__ == "__main__":
    asyncio.run(main())