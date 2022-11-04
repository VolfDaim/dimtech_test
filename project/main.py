from databases import Database
from sanic import Sanic
from environs import Env
from sqlalchemy.ext.asyncio import create_async_engine

from project.middleware import setup_middlewares
from project.routes import setup_routes

app = Sanic("DimaTechTestApp")

bind = create_async_engine('postgresql+asyncpg://postgres:123@localhost:5432/postgres', echo=True)


def database():
    app.ctx.db = Database('postgresql://postgres:123@localhost:5432/postgres')

    @app.listener('after_server_start')
    async def connect_to_db(app, loop):
        await app.ctx.db.connect()

    @app.listener('after_server_stop')
    async def diconnect_from_db(*args, **kwargs):
        await app.ctx.db.disconnect()


env = Env()
env.read_env()

app.config.DEBUG = True
app.config.HOST = '0.0.0.0'
app.config.PORT = 8000
app.config.DB_URL = 'postgresql://postgres:123@localhost:5432/postgres'

database()
setup_routes(app, bind)
setup_middlewares(app, bind)
