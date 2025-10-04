from flask import Flask # , jsonify, request
from flask_smorest import Api

from db import db # stores, items
import models 

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint

import os

# With factory pattern, we write a function that returns the app
# We also pass configration values to the function
def create_app(db_url = None):

    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] =  "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdlivr.net/npm/swagger-ui-dist"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URI", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    @app.before_request
    def create_tables():
        db.create_all()

    # with app.app_context():
    #     db.create_all()

    app.logger.setLevel("INFO")

    api = Api(app)
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)

# import os

# @app.get("/")  # optional, to quiet the 404 on /
# def root():
#     return {"ok": True}

# @app.get("/store")
# def get_stores():
#     return jsonify({"Prining list of stores as JSON object:": list(stores.values())})

# @app.post("/store")
# def create_store():
#     store_data = request.get_json()
#     print(store_data, flush=True)
#     if "name" not in store_data:
#         abort(400, 
#               message="Bad request. Ensure 'name' is included in the JSON object")
#     for store in stores.values():
#         if store_data["name"] == store["name"]:
#             abort(400, message="Store already exists")
#     store_id = uuid.uuid4().hex
#     print(store_data, flush=True)
#     store = {**store_data, "id": store_id}  
#     # ** is kwargs, it unpacks the values of store_data dictionary and 
#     # include them in the new dictionary new_store
#     stores[store_id] = store
#     return store, 201

# # Check if the store exists and add to the store
# # Note that now item and store are different independent entities
# # We need to create them separately and link them. No longer shall
# # we create them wiith reference to one another. But for now we are
# # still checking that the item is not orphaned, user has sent a
# # store_id for keeping that item
# @app.post("/item")
# def create_item():
#     item_data = request.get_json()
#     print(item_data, flush=True)
#     # JSON body should have data on price, store_id and name to create item
#     if ("price" not in item_data) or ("store_id" not in item_data) or ("name" not in item_data):
#         abort(400, message="Bad request, Ensure 'price', 'store_id', and 'name' are included in the JSON payload")
#     # There must not be duplicate names in the same store
#     print("Passed the first test", flush=True)
#     for item in items.values():
#         if (item_data["name"] == item["name"]) and (item_data["store_id"] == item["store_id"]):
#             abort(400, message="Item already exists")
#     print("Passed the second test", flush=True)
#     # Else we will create an item within that store which was sent from Front End
#     item_id = uuid.uuid4().hex
#     item = {**item_data, "Item_id": item_id}
#     items[item_id] = item
#     return item, 201

# # Getting all items: Now we no longer need to iterate of stores
# @app.get("/item")
# def get_all_items():
#     return {"items": list(items.values())}

# # Check for the store name and return only the items in the store
# @app.get("/item/<string:item_id>")
# def get_item(item_id):
#     print(f"From app.get_item() EP/API, item_id: {item_id}", flush=True)
#     # request_data = request.get_json()  
#     # We can not call get_json in a GET request. JSON body can only be passed through a POST request
#     # print(f"Responding from get_store() {request_data}", flush=True)
#     try:
#         return items[item_id]  # Flask jsonify the response
#     except KeyError:
#         abort(404, message="Item not found")

# @app.delete("/item/<string:item_id>")
# def delete_item(item_id):
#     try:
#         del items[item_id]
#         return {"message": "Item deleted"}
#     except KeyError:
#         abort(404, message="Item not found")

# # Iterating of individual stores
# @app.get("/store/<string:store_id>")
# def get_store(store_id):
#     print("From app.get_store() EP/API", flush=True)
#     # print(stores[store_id], flush=True)
#     try:
#         return stores[store_id]  # Flask jsonify the response
#     except KeyError:
#         abort(404, message="Store not found")

# @app.put("/item/<string:item_id>")
# def update_item(item_id):
#     item_data = request.get_json()  # Get from the JSON body
#     print(item_id, flush=True)
#     print(item_data, flush=True)
#     if ("price" not in item_data) or ("name" not in item_data):
#         abort(400, message="Bad request. Ensure 'price' and 'name' are included in the JSON payload")
#     print("Passed the first test", flush=True)
#     try:
#         item = items[item_id]
#         item |= item_data
#         return item
#     except KeyError:
#         abort(400, message="Item not found")