from contextlib import contextmanager


from sanic.response import json, text
from sqlalchemy import select, insert
from sqlalchemy.orm import sessionmaker

from project.logic.user import create_user
from project.marshmallow.product_schema import ProductResultSchema
from project.models import Product, Base


def setup_routes(app, bind):
    DBSession = sessionmaker(
        binds={
            Base: bind,
        },
        expire_on_commit=False,
    )

    @contextmanager
    def session_scope():
        """Provides a transactional scope around a series of operations."""
        session = DBSession()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @app.get("/products")
    async def product_list(request):
        session = request.ctx.session
        async with session.begin():
            stmt = select(Product)
            result = await session.execute(stmt)
            product = result.all()
        schema = ProductResultSchema(many=True)
        return json(schema.dump([pr[0] for pr in product]))

    @app.post("/products")
    async def create_product(request):
        data = request.json
        session = request.ctx.session
        async with session.begin():
            stmt = insert(Product).values(name=data["name"],
                                          description=data["description"],
                                          price=data["price"])
            await session.execute(stmt)
        return json(data)

    @app.post("/register")
    async def register(request):
        data = request.json
        username = data["username"]
        fullname = data["fullname"]
        password = data["password"]

        session = request.ctx.session
        result = await create_user(username, password, fullname, session)
        return result

    @app.get("/login")
    async def login(request):
        data = request.json
        session = request.ctx.session
        result = await log_user(data, session)
        return result

