import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import StoreSchema
from models import StoreModel
from db import db

from sqlalchemy.exc import IntegrityError, SQLAlchemyError

# Note: Blueprint from smorest is used to divide an API into multiple
# segments
blp = Blueprint("stores", __name__, description = "Operations on stores")  # Dundername for each blueprint

# flask MethodView is going to create a class
# Note that we want to route the requests to get_store(store_id)
# through methods of this class
# Note that for one End Point one Blueprint decorator is used, but blp.route() method
# is used in all cases
# Note a critical distinction: functions with BluePrint are defined just with get(),
# delete(), post(), etc. Like get_stores() is defined with get() only as it 
# recieves data through get type request object
@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store
        # print("From app.get_store() EP/API", flush=True)
        # print(stores[store_id], flush=True)

    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        try:
            db.session.delete(store)
            db.session.commit()
            return {"message": "Stores deleted"}, 200
        except KeyError:
            abort(404, message="Item not found")

@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()
    
    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def post(self, store_data):
        # store_data = request.get_json()
        # print(store_data, flush=True)
        # if "name" not in store_data:
        #     abort(400, 
        #         message="Bad request. Ensure 'name' is included in the JSON object")
        # for store in stores.values():
        #     if store_data["name"] == store["name"]:
        #         abort(400, message="Store already exists")
        # store_id = uuid.uuid4().hex
        # print(store_data, flush=True)

        store = StoreModel(**store_data) 
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort (400, message="A store with that name alrady exists.")
        except SQLAlchemyError:
            abort(400, message="An error ocurred creating the store.")
        # ** is kwargs, it unpacks the values of store_data dictionary and 
        # include them in the new dictionary new_store
        # stores[store_id] = store

        return store, 201