from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
import os 

#TODO: Comments
MIGRATION_DIR = os.path.join('app', 'migrations')

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
db.create_all()
migrate = Migrate(app, db, directory=MIGRATION_DIR)

# Will add records to our database when function is called
def _update_db(obj):
    db.session.add(obj)
    db.session.commit()
    return obj

# Will delete records when function is called
def _delete_record(user, ticker):
    db.session.delete(user)
    # if ticker == None then it's removing a single ticker
    # Whereas .delete() will delete all records in a column
    if ticker != None:
        db.session.query(ticker).delete()
    db.session.commit()


# keep at bottom to avoid circular dependencies when starting Flask server
# app and db objects need to be instantiated before the entire file can be loaded by Flask
from app import routes, models
