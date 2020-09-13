from app import db


class User(db.Model):
    __tablename__ = 'users'

    phone_number = db.Column(db.String(), primary_key=True)
    tickers = db.relationship(
        "Tickers",
        backref="user",
        primaryjoin="User.phone_number == Tickers.user_id",
    )
    adding_tickers = db.cOlumn(db.Boolean())

    def __init__(self, phone_number):
        self.phone_number = phone_number
        self.adding_tickers = False


class Tickers(db.Model()):
    __tablename__ = "tickers"

    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String())
    # to join with User table
    user_id = db.Column(db.Text(), db.ForeignKey("users.phone_number"))

    def __init__(self, user_id, front, back):
        self.user_id = user_id
        self.ticker = ticker
