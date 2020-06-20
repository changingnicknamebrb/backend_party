import asyncio
import pymysql
import aiohttp_cors
from aiohttp import web

#Работа с SQL
con = pymysql.connect('localhost', 'coolname', 'cool', 'one', cursorclass=pymysql.cursors.DictCursor)

#Работа с HTTP-requests
async def getProfile(request):
    with con:
        cur = con.cursor()
        data = request.query
        cur.execute("SELECT * FROM usersinfo WHERE `id` = {}".format(data['id']))
        rows = cur.fetchall()
        if rows.__len__() != 0:
            return web.json_response({'success': True,
                                    'id': rows[0]['id'],
                                    'firstname': rows[0]['firstname'], 
                                    'lastname': rows[0]['lastname'], 
                                    'height': rows[0]['height'], 
                                    'weight': rows[0]['weight'], 
                                    'information': rows[0]['information'], 
                                    'birth_date': rows[0]['birth_date'].strftime("%d-%m-%Y")})
        else:
            return web.json_response({'success': False})

async def registrate(request):
    with con:
        cur = con.cursor()
        data = await request.post()
        cur.execute(
            "INSERT INTO `usersinfo` (`id`, `firstname`, `lastname`, `height`, `weight`, `information`, `birth_date`) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}');".format(
                data['id'], data['firstname'], data['lastname'], data['height'], data['weight'], data['information'], data['birth_date']))
        return web.json_response({'success': True})

async def changeProfile(request):
    with con:
        cur = con.cursor()
        data = await request.post()
        for item in data:
            if item != 'id':
                cur.execute("UPDATE `usersinfo` SET `{0}` = '{1}' WHERE `id` = {2};".format(item, data[item], data['id']))
        return web.json_response({'success': True})

async def createEvent(request):
    with con:
        cur = con.cursor()
        data = await request.post()
        cur.execute(
            "INSERT INTO `events` (`users`, `creator`, `name`, `description`, `track_id`) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}');".format(
                data['users'], data['creator'], data['name'], data['description'], data['track_id']))
        return web.json_response({'success': True})

async def changeEvent(request):
    with con:
        cur = con.cursor()
        data = await request.post()
        for item in data:
            if item != 'id':
                cur.execute("UPDATE `events` SET `{0}` = '{1}' WHERE `id` = {2};".format(item, data[item], data['id']))
        return web.json_response({'success': True})

async def getEvents(request):
    return web.Response(text="Hello, world2")

async def removeEvent(request):
    with con:
        cur = con.cursor()
        data = request.query
        cur.execute("DELETE FROM `events` WHERE `id`= {}".format(data['id']))
        return web.json_response({'success': True})


app = web.Application()

cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
})

resource = cors.add(app.router.add_resource("/autorize"))
cors.add(resource.add_route("GET", getProfile))
resource = cors.add(app.router.add_resource("/getProfile"))
cors.add(resource.add_route("GET", getProfile))
resource = cors.add(app.router.add_resource("/registrate"))
cors.add(resource.add_route("POST", registrate))
resource = cors.add(app.router.add_resource("/changeProfile"))
cors.add(resource.add_route("POST", changeProfile))
resource = cors.add(app.router.add_resource("/createEvent"))
cors.add(resource.add_route("POST", createEvent))
resource = cors.add(app.router.add_resource("/changeEvent"))
cors.add(resource.add_route("POST", changeEvent))
resource = cors.add(app.router.add_resource("/getEvents"))
cors.add(resource.add_route("GET", getEvents))
resource = cors.add(app.router.add_resource("/removeEvent"))
cors.add(resource.add_route("POST", removeEvent))


web.run_app(app, host = '141.101.196.166', port=8080)
