import asyncio
import pymysql
from aiohttp import web

#Работа с SQL
con = pymysql.connect('localhost', 'root', 'root', 'test', cursorclass=pymysql.cursors.DictCursor)

with con:
    cur = con.cursor()
#    cur.execute("INSERT INTO `usersinfo` (`idusers`, 'name') VALUES ({0}, {1});".format('1234', 'John'))         #Добавить запись в таблицу
#    cur.execute("SELECT * FROM usersinfo")                                                                       #Выбрать все записи из таблицы. * - получить все столбцы, иначе в '' пишем название столбца. Получить определённые записи - WHERE *условие*
#    rows = cur.fetchall()                                                                                    #
#    for row in rows:                                                                                         #
#        print(row['idusers'], '   ', row['name'])                                                            #
#    cur.execute("UPDATE `users` SET `name` = 'Now I'm Victor' WHERE `id` = 1234;")                           #Изменяем значение в таблице users в столбце name с id = 1234
#    cur.execute("DELETE FROM `users` WHERE `idusers`= 123")                                                  #Удаляем ряд в таблице users с id = 123


#Работа с HTTP-requests
async def getProfile(request):
    with con:
        cur = con.cursor()
        data = requestquery
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
app.add_routes([web.get('/autorize', getProfile)])
app.add_routes([web.get('/getProfile', getProfile)])
app.add_routes([web.post('/registrate', registrate)])
app.add_routes([web.post('/changeProfile', changeProfile)])
app.add_routes([web.post('/createEvent', createEvent)])
app.add_routes([web.post('/changeEvent', changeEvent)])
app.add_routes([web.get('/getEvents', getEvents)])
app.add_routes([web.post('/removeEvent', removeEvent)])


web.run_app(app)
