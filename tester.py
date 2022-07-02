import asyncio
from aiohttp import web
import BAC0


async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)

async def start_api_server():
    print("api")
    loop = asyncio.get_event_loop()
    app = web.Application()
    app.add_routes([web.get('/', handle),
                    web.get('/{name}', handle)])
    #web.run_app(app)
    runner = web.AppRunner(app)
    await runner.setup()
    await loop.create_server(runner.server, '127.0.0.1', 8080)
    print('Server started at http://127.0.0.1:8080...')

async def action():
    print("action")
    bacnet = BAC0.lite()
    while True:
        pass


async def main():
    #await action()
    await(asyncio.gather(start_api_server(), action()))

if __name__ == '__main__':
    asyncio.run(main())