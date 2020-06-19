import asyncio
from aiohttp import web

async def hello1(request):
    return web.Response(text="Hello, world1")

async def hello2(request):
    return web.Response(text="Hello, world2")

async def hello3(request):
    data = await request.post()
    return web.Response(text="Hello, {} {}".format(data['name'], data['surname']))

app = web.Application()
app.add_routes([web.get('/1', hello1)])
app.add_routes([web.get('/2', hello2)])
app.add_routes([web.post('/3', hello3)])

<<<<<<< HEAD
web.run_app(app)
=======
web.run_app(app)
>>>>>>> a712aa847e8ba43cad0632e741b3b496edba5e7a
