from marshmallow import fields
from marshmallow.schema import BaseSchema


class CreateProductSchema(BaseSchema):
    name = fields.String(required=True)
    description = fields.String(required=False)
    price = fields.Integer(required=True)


class UpdateProductSchema(BaseSchema):
    name = fields.String(required=True)
    description = fields.String(required=False)
    price = fields.Integer(required=True)


class ProductResultSchema(BaseSchema):
    id = fields.UUID(required=True)
    name = fields.String(required=True)
    description = fields.String(required=False)
    price = fields.Integer(required=True)
