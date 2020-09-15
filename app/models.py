from app import db
import random

#TODO: Comments

class User(db.Model):
    __tablename__ = "users"

    phone_number = db.Column(db.Text, primary_key=True)
    tickers = db.relationship('Ticker', backref='user', primaryjoin="User.phone_number == Ticker.user_id")
    
    def __init__(self, phone_number):
        self.phone_number = phone_number

class Ticker(db.Model):
    __tablename__ = "tickers"
    
    id = db.Column(db.Integer, primary_key=True)
    tickers = db.Column(db.Text(), nullable=True)
    user_id = db.Column(db.Text(), db.ForeignKey('users.phone_number'))
    
    def __init__(self, user_id, tickers):
        self.user_id = user_id
        self.tickers = tickers
        
        
