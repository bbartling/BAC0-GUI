from aiohttp.web import Application, json_response, middleware
import asyncio
from pathlib import Path
from aiohttp_pydantic import PydanticView
from aiohttp import web
from aiohttp_pydantic import oas


from views import ReadSingleView,WriteSingleView,ReleaseSingleView
from views import ReadMultView,WriteMultView,ReleaseMultView



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
web.run_app(app, host='0.0.0.0', port=8080)





