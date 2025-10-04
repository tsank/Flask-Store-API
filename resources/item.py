from sqlite3 import IntegrityError
import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema

# from db import items

blp = Blueprint("Items", __name__, description = "Operations on items.")

@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item

    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        try:
            db.session.delete(item)
            db.session.commit()
            return {"message": "Item deleted"}, 204
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(500, message=f"Datbase error: {str(e)}")

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)        # Response schema should be below argument schema
    def put(self, item_data, item_id):    # Injected arguments come first
        # item = ItemModel.query.get_or_404(item_id)
        created = False

        item = ItemModel.query.get(item_id)
        # Note get_or_404() never returns null, it either returns the object item_id or an error
        # Thus if we use get_or_404(), there is no need to create if..else construct
        # In case we use if..else construct, let's use get() instead of get_or_404()
        # if item:
        #     item.price = item_data["price"]
        #     item.name = item_data["name"]
        # else:
        #     item = ItemModel(id=item_id, **item_data)
        #     created = True
        if item:
            # Update only what was provided
            for k, v in item_data.items():
                setattr(item, k, v)
        else:
            item = ItemModel(id=item_id, **item_data)
            created = True
            db.session.add(item)
        
        try:
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            abort(409, message="Conflict: constraint/duplicate violation.")
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(500, message=f"Database error: {str(e)}")

        return (item, 201) if created else item
        
        # raise NotImplementedError("Updating an item is not implemented.")
        # item_data = request.get_json()  # Not needed since data comes through ItemUpdateSchema
        # print(item_id, flush=True)
        # print(item_data, flush=True)
        # if ("price" not in item_data) or ("name" not in item_data):
        #     abort(400, message="Bad request. Ensure 'price' and 'name' are included in the JSON payload")
        # print("Passed the first test", flush=True)  

        # try:
        #     item = items[item_id]
        #     item |= item_data
        #     return item
        # except KeyError:
        #     abort(404, message="Item not found")   

@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()   # Note that the output changes to list due to marshowmallow
    
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        # These validations are addressed by marshmallow
        # item_data = request.get_json()
        # print(item_data, flush=True)
        # # JSON body should have data on price, store_id and name to create item
        # if ("price" not in item_data) or ("store_id" not in item_data) or ("name" not in item_data):
        #     abort(400, message="Bad request, Ensure 'price', 'store_id', and 'name' are included in the JSON payload")
        # # There must not be duplicate names in the same store
        # print("Passed the first test", flush=True)

        # Marshmallow can not check whether an item already exists so we need to keep these validations
        # for item in items.values():
        #     if (item_data["name"] == item["name"]) and (item_data["store_id"] == item["store_id"]):
        #         abort(400, message="Item already exists")
        # print("Passed the second test", flush=True)
        # Else we will create an item within that store which was sent from Front End

        # item_id = uuid.uuid4().hex
        # item = {**item_data, "item_id": item_id}
        # items[item_id] = item

        item = ItemModel(**item_data)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error ocurred while inserting the item")

        return item, 201