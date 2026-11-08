from marshmallow import Schema, fields, validate

# --- Product Schemas ---
class ProductOut(Schema):
    id = fields.Int(dump_only=True)
    sku = fields.Str()
    name = fields.Str()
    description = fields.Str(allow_none=True)
    price_cents = fields.Int()
    qty_in_stock = fields.Int()
    archived = fields.Bool()

class ProductIn(Schema):
    sku = fields.Str(required=True, validate=validate.Length(min=3, max=32))
    name = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    price_cents = fields.Int(required=True, validate=validate.Range(min=0))
    qty_in_stock = fields.Int(load_default=0, validate=validate.Range(min=0))

class ProductPatch(Schema):
    name = fields.Str()
    price_cents = fields.Int(validate=validate.Range(min=0))

class ReserveIn(Schema):
    qty = fields.Int(required=True, validate=validate.Range(min=1))

class ProductQueryArgsSchema(Schema):
    page = fields.Int(load_default=1, validate=validate.Range(min=1))
    size = fields.Int(load_default=20, validate=validate.Range(min=1, max=100))

class ProductListOut(Schema):
    items = fields.List(fields.Nested(ProductOut))
    page = fields.Int()
    size = fields.Int()
    total = fields.Int()

# --- Order Schemas ---
class OrderItemIn(Schema):
    product_id = fields.Int(required=True)
    qty = fields.Int(required=True, validate=validate.Range(min=1))

class OrderIn(Schema):
    items = fields.List(fields.Nested(OrderItemIn), required=True, validate=validate.Length(min=1))

class OrderItemOut(Schema):
    product_id = fields.Int()
    qty = fields.Int()
    price = fields.Int(attribute="price_cents")

class OrderOut(Schema):
    id = fields.Int(dump_only=True)
    status = fields.Str()
    items = fields.List(fields.Nested(OrderItemOut))
    
class OrderListOut(Schema):
    items = fields.List(fields.Nested(OrderOut))
