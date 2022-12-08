from marshmallow import fields
from marshmallow import Schema


class RealtyParametersSchema(Schema):
    city = fields.String(required=True)
    details = fields.List(fields.String(), required=True)
    state = fields.String(required=True)
    street_address = fields.String(required=True)
    unit = fields.String(required=False)
    zip = fields.Int(required=True)
