from marshmallow import Schema, fields

class PlainItemSchema(Schema):
    id = fields.Int(dump_only=True)       # Only send, no receive
    name = fields.Str(required=True)      # Must be in the JSON payload
    price = fields.Float(required=True)
    # store_id = fields.Str(required=True)

class ItemUpdateSchema(Schema):
    name = fields.Str()                   # These are optional so can be missing
    price = fields.Float() 
    store_id = fields.Int()

class PlainStoresSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()

class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(PlainStoresSchema(), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)

class StoreSchema(PlainStoresSchema):
    items = fields.List(fields.Nested(PlainItemSchema), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)

class TagSchema(PlainTagSchema):
    store_id = fields.Int(load_only=True)
    store = fields.Nested(PlainStoresSchema, dump_only=True)
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)

class TagAndItemSchema(Schema):
    message = fields.Str()
    item = fields.Nested(ItemSchema)
    tag = fields.Nested(TagSchema)

# Note that PlainSchemas are flat and has not nesting
# Nesting happens when Item includes it's Store and Store also includes it's Item
# This results in an infinite loop: Item -> Store -> Item -> Store -> ...
# To prevent that we use PlainSchemas which do not allow any nesting
# When we use nesting after that, we use PlainSchemas, thus
# fields.Nested(PlainItemSchema). Note that PlainItemSchema is not
# nested so that nesting stops after one level and there are no
# inifinite loop formed

# id = fields.Int(dump_only=True) means that id is read only for the user
# and it will appear in the outputs the api sends to the client (serialization="dump"),
# schema.dumps(obj) or decorators like @blp.response(...) in flask_smorest
# which call dump under the hood.
# Load = deserialize incloming JSON -> Python types used in the app which 
# comes from HTTP request object, schema.Load(), schema.loads(data)
# or @blp.arguments(Schema). 
# Typically Dump and Load are opposite terms, Dump is dumpted on user
# Load is taken up by the application. Dump follows only response objects
# and Load follows only request objects.
# dump_only=True ensures that clients see 'id' but they can not set 'id'
# Server generated fields: dump_only=True
# Sensitive input only fields like password: load_only=True so that
# these are never echoed back