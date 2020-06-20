import asyncio
import pymysql
from aiohttp import web
#Работа с SQL
con = pymysql.connect('localhost', 'root', 
    'root', 'test', cursorclass=pymysql.cursors.DictCursor)

with con:
    cur = con.cursor()
    cur.execute("INSERT INTO `users` (`idusers`, 'name') VALUES ({0}, {1});".format('1234', 'John'))         #Добавить запись в таблицу
    cur.execute("SELECT * FROM users")                                                                       #Выбрать все записи из таблицы. * - получить все столбцы, иначе в '' пишем название столбца. Получить определённые записи - WHERE *условие*
    rows = cur.fetchall()                                                                                    #
    for row in rows:                                                                                         #
        print(row['idusers'], '   ', row['name'])                                                            #
    cur.execute("UPDATE `users` SET `name` = 'Now I'm Victor' WHERE `id` = 1234;")                           #Изменяем значение в таблице users в столбце name с id = 1234
    cur.execute("DELETE FROM `users` WHERE `idusers`= 123")                                                  #Удаляем ряд в таблице users с id = 123


#Работа с HTTP-requests
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


web.run_app(app)
