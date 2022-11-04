from uuid import uuid4

import sqlalchemy
from sqlalchemy import Column, create_engine
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship

metadata = sqlalchemy.MetaData()
Base = declarative_base()
engine = create_engine('postgresql://postgres:123@localhost:5432/postgres')


class Users(Base):
    __tablename__ = 'users_table'
    id = Column('id', UUID(as_uuid=True), default=uuid4, primary_key=True)
    username = Column('username', sqlalchemy.String(length=100), unique=True)
    fullname = Column('fullname', sqlalchemy.String(length=200))
    password = Column('password', sqlalchemy.String(length=256))
    check = relationship("Check")

    def json(self):
        return {
            "id": self.id,
            "username": self.username,
            "fullname": self.fullname,
        }

class Product(Base):
    __tablename__ = 'product_table'
    id = Column('id', UUID(as_uuid=True), default=uuid4, primary_key=True)
    name = Column('name', sqlalchemy.String(length=100))
    description = Column('description', sqlalchemy.String(length=500))
    price = Column('price', sqlalchemy.Integer)

    def to_dict(self):
        return {"name": self.name, "description": self.description}

    @classmethod
    async def create(cls, conn, values):
        cur = await Product.insert().values(**values).returning(Product.__table__).execute(conn)


class Check(Base):
    __tablename__ = 'check_table'
    id = Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    balance = Column('balance', sqlalchemy.Integer)
    user = Column(UUID, sqlalchemy.ForeignKey('users_table.id'))
    transaction = relationship("Transaction")


class Transaction(Base):
    __tablename__ = 'transaction_table'
    id = Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    summ = Column(sqlalchemy.Integer)
    check = Column(UUID, sqlalchemy.ForeignKey('check_table.id'))
