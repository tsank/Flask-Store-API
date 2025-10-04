from db import db

class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique = True, nullable=False)

    items = db.relationship("ItemModel", \
                            back_populates="store", lazy="dynamic", cascade="all, delete")  
    # No pre-fetching of stores from items
    # Note that since there is one (store) to many (items) relationship,
    # we use object name 'items' with db.relationship() in store.py
    # while we use object name 'store' with db.relationship() in item.py

    # Note that lazy="dynamic" enables items attribute to resolve to
    # a SQLAlchemy query and without that it resolves to a list of items

    # Note cascade = "all, delete" removes the items associated with the store as well

    tags = db.relationship("TagModel", back_populates = "store", lazy = "dynamic")
