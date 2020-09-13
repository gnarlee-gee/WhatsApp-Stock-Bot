from app import db, _update_db
import random


class User(db.Model):
    __tablename__ = "users"

    phone_number = db.Column(db.Text, primary_key=True)
    tickers = db.Column(db.String())
    
    def __init__(self, phone_number):
        self.phone_number = phone_number
