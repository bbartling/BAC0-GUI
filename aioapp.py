from aiohttp.web import Application, json_response, middleware
import asyncio
import argparse
from pathlib import Path
from aiohttp_pydantic import PydanticView
from aiohttp import web
from aiohttp_pydantic import oas


from views import ReadSingleView,WriteSingleView,ReleaseSingleView
from views import ReadMultView,WriteMultView,ReleaseMultView



my_parser = argparse.ArgumentParser(description='Run RestApi App as localhost or seperate device')
my_parser.add_argument('-ip',
                       '--host_address',
                       required=False,
                       type=str,
                       default='0.0.0.0',
                       help='To run as localhost only:$ python3 aioapp.py -ip localhost')
                       
my_parser.add_argument('-port',
                       '--port_number',
                       required=False,
                       type=int,
                       default=5000,
                       help='To change port run:$ python3 aioapp.py -port 8080')                      
args = my_parser.parse_args()

host_address = args.host_address
port_number = args.port_number

print('Running Rest App On Address ' + host_address)
print('Running Rest App On Port ' + str(port_number))



@middleware
async def _not_found_to_404(request, handler):
    try:
        return await handler(request)
    except Exception as error:
        return json_response({"key_error": f"{error}"}, status=404)



app = Application(middlewares=[_not_found_to_404])
oas.setup(app, version_spec="1.0.1", title_spec="BACnet Rest API App")




app.router.add_view('/bacnet/read/single', ReadSingleView)
app.router.add_view('/bacnet/read/multiple', ReadMultView)
app.router.add_view('/bacnet/write/single', WriteSingleView)
app.router.add_view('/bacnet/write/multiple', WriteMultView)
app.router.add_view('/bacnet/release/single', ReleaseSingleView)
app.router.add_view('/bacnet/release/multiple', ReleaseMultView)
web.run_app(app, host=host_address, port=port_number)





