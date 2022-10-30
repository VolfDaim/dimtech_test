
import sqlmodel
from aiopg import create_pool
from databases import Database
from sanic import Sanic
from environs import Env
from sqlalchemy.ext.asyncio import create_async_engine

from project.settings import Settings

app = Sanic("DimaTechTestApp")
app.extend()

def database():
    @app.listener('before_server_start')
    async def connect_to_db(app,loop):
        conn = "postgresql://postgres:123@localhost:5432/postgres"
        app.config['pool'] = await create_pool(
            dsn=conn,
            min_size=10,  # in bytes,
            max_size=10,  # in bytes,
            max_queries=50000,
            max_inactive_connection_lifetime=300,
            loop=loop)

    @app.listener('after_server_stop')
    async def diconnect_from_db(*args, **kwargs):
        await app.db.disconnect()


def init():
    env = Env()
    env.read_env()

    app.config.from_object(Settings)
    database()
    app.run(
        host=app.config.HOST,
        port=app.config.PORT,
        debug=app.config.DEBUG,
        auto_reload=app.config.DEBUG,
    )
