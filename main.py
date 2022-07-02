from aiohttp.web import Application, json_response, middleware
from aiohttp_basicauth import BasicAuthMiddleware
import argparse
from pathlib import Path
from aiohttp_pydantic import PydanticView
from aiohttp import web
from aiohttp_pydantic import oas


from views import ReadSingleView,WriteSingleView,ReleaseSingleView
from views import ReadMultView,WriteMultView,ReleaseMultView

from bacnet_actions import bac0_app

bac0_app.run()

my_parser = argparse.ArgumentParser(description='Run RestApi App as localhost or seperate device')
                       
my_parser.add_argument('-port',
                       '--port_number',
                       required=False,
                       type=int,
                       default=5000,
                       help='To change port run:$ python3 aioapp.py -port 8080')

my_parser.add_argument('-use_auth',
                       '--use_authentication',
                       required=False,
                       type=bool,
                       default=False,
                       help='boolean to use authentication for rest gateway')

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


args = my_parser.parse_args()

port_number = args.port_number
auth_username = args.auth_username
auth_password = args.auth_password
use_authentication = args.use_authentication

print('Running Rest App On Port ' + str(port_number))



@middleware
async def _not_found_to_404(request, handler):
    try:
        return await handler(request)
    except Exception as error:
        return json_response({"key_error": f"{error}"}, status=404)


if use_authentication:
    auth = BasicAuthMiddleware(username=auth_username, password=auth_password)
    app = Application(middlewares=[_not_found_to_404,auth])
    print('Running Rest App http basic authentication username ' + str(auth_username))
    print('Running Rest App http basic authentication password ' + str(auth_password))
    
else:
    app = Application(middlewares=[_not_found_to_404])
    print('Running Rest App http with no authentication')


# open API splash screen
oas.setup(app, version_spec="1.0.1", title_spec="BACnet Rest API App")


app.router.add_view('/bacnet/read/single', ReadSingleView)
app.router.add_view('/bacnet/read/multiple', ReadMultView)
app.router.add_view('/bacnet/write/single', WriteSingleView)
app.router.add_view('/bacnet/write/multiple', WriteMultView)
app.router.add_view('/bacnet/release/single', ReleaseSingleView)
app.router.add_view('/bacnet/release/multiple', ReleaseMultView)
web.run_app(app, port=port_number)

