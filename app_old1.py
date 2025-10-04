from flask import Flask, jsonify, request


app = Flask(__name__)

app.logger.setLevel("INFO")  # or DEBUG

stores = [
    {
        "name": "My store",
        "items": [
            {
                "name": "chair",
                "price": 15.99
            }
        ]
    }
]

@app.get("/")  # optional, to quiet the 404 on /
def root():
    return {"ok": True}

@app.get("/store")
def get_stores():
    return jsonify({"Prining list of stores as JSON object:": stores})

@app.post("/store")
def create_store():
    request_data = request.get_json()
    print(request_data, flush=True)
    new_store = {"name": request_data["name"], "items":[]}
    stores.append(new_store)
    return new_store, 201

# Check if the store exists and add to the store
@app.post("/store/<string:name>/item")
def create_item(name):
    request_data = request.get_json()
    for store in stores:
        if store["name"]==name:
            new_item = {"name": request_data["name"], "price": request_data["price"]}
            store["items"].append(new_item)
            return new_item, 201
    return {"message": "Store not found"}, 404

# Check for the store name and return only the items in the store
@app.get("/store/<string:name>/item")
def get_store(name):
    print("From app.get() EPI", flush=True)
    # request_data = request.get_json()  
    # We can not call get_json in a GET request. JSON body can only be passed through a POST request
    # print(f"Responding from get_store() {request_data}", flush=True)
    for store in stores:
        if store["name"] == name:
            return {"Returning items": store["items"]}
    return {"message": "Store not found"}, 404



if __name__ == "__main__":
    app.run(debug=True)