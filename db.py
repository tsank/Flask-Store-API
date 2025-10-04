# stores = {}
# items = {}

# Now we no longer need stores and items dictionaries as we will be using relational databases
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Note"
# db.Model - Base class for ORM models
# db.Column - Column and field definition
# db.Foreignkey
# db.relationship - Defines relationship between tables
# db.Table - For association across tables (many to many)
# db.Session - Unit of Work (UoW: Add/Commit/Rollback, run selects/SQL)
# db.Session.add(user), db.Session.commit()
# rows = db.session.execute(db.select(user).where(User.name=="Ram")).sclars.all()
# with app.app_context():
#   db.create_all()
# db.init_app(app)
# db.Integer, db.Float, db.Str, ...