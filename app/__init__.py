from app import routes, models
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


def _update_db(obj):
    ''' Updates database when user makes changes '''
    db.session.add(obj)
    db.session.commit()
    return obj
