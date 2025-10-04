from db import db   # Note that db = SQLAlchemy() is defined in db.py; we are no longer using the dictionaries items{} and stores{}

class ItemModel(db.Model):
    __tablename__ = "items"    # __table__ lets us bind the class ItemModel inhetited from db.Model to table object "items" directly. 
    # __table__ is an alternative to __tablename__, however in __table__ we need to supply the table, while in __tablename__ we can create the table ourselves

    id = db.Column(db.Integer, primary_key=True)  # the table is auto-increamenting
    name = db.Column(db.String(80), unique=True, nullable=False)    # nullable means that this column must be there in a row
    price = db.Column(db.Float(precision=2), unique=False, nullable=False)
    store_id = db.Column(
        db.Integer, db.ForeignKey("stores.id"), unique=False, nullable=False
        )    # Foreign key to stores table, this will prevent creating an item without a connecting foreign key
    store = db.relationship("StoreModel", back_populates="items")
    tags = db.relationship("TagModel", back_populates="items", secondary="items_tags")

