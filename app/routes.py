from flask import request
# from app import app, _update_db, _delete_record, db
from app import app, _update_db, _delete_record
from app.models import User, Ticker
from twilio.twiml.messaging_response import MessagingResponse
from iexfinance.stocks import Stock
import random
import os

# Use these to show if price is up or down -> 🟩🟥
# TODO: Format 'show' command *TICKER*: Price

# The bot's response
def _send_message(output_lines):
    '''this functions takes in a list and creates a message by joining 
    each item in the list and returns a string'''
    resp = MessagingResponse()
    msg = resp.message()
    msg.body("\n".join(output_lines))
    return str(resp)


@app.route("/bot", methods=["POST"])
def bot():
    ''' handles incoming messages, gets and creates remote_number (our general id), and initializes 
    response list'''
    incoming_msg = request.values.get("Body", "").strip().lower()
    remote_number = request.values.get("From", "").lower()
    output_lines = []
    # incoming From is "whatsapp:phone number/acct id"
    if remote_number.startswith("whatsapp:"):
        remote_number = remote_number.split(":")[1]

    # if no phone number then assign a random number for a primary key
    if not remote_number:
        remote_number = str(random.randrange(1000000))


    user = User.query.get(remote_number)
    # our commands
    # returns a list of commands to bot's response (_send_message())
    if incoming_msg == "help" or incoming_msg.lower() == "hi":
        if not user:
            output_lines.append("Greetings stranger! Please create an account.")
        else:
            output_lines.append(f"Greetings *{user.phone_number}*! Here are my commands.")
        output_lines.append("'create account' - new users must create a new account")
        output_lines.append("'add ticker1 ticker2 ... tickerN' - adds any amount of tickers to your account")
        output_lines.append("\t*example: add TSLA AAPL NVDA*")
        output_lines.append("'remove ticker1 ticker2 ... tickerN' - removes selected tickers from account")
        output_lines.append("\t*example: remove TSLA NVDA*")
        output_lines.append("'show' - displays market prices of stocks in your portfolio")
        output_lines.append("'delete account' - deletes your account")
        return _send_message(output_lines)
    
    
    # creates account with primary key = phone number
    # if no user is found in the query we create a new one
    if not user:
        if incoming_msg == "create account":
            new_user = User(remote_number)
            _update_db(new_user)
            output_lines.append(
                f"Account successfully created for number *{remote_number}*!"
                )
            output_lines.append(
                "Text 'help' at any time to see available commands."
            )
        else:
            output_lines.append("Please register with 'create account', first!") # have to create an acct before doing other commands
        return _send_message(output_lines)
    else: # if there is a user already in db and they typed create, go here to let them know they can begin
        if incoming_msg == "create account":
            output_lines.append(
                f"You have already registered *{remote_number}*. Begin typing some commands!\nType 'help' for commands!."
                )
            return _send_message(output_lines) # send the response

    # deletes user's account
    if incoming_msg == "delete account":
        _delete_record(user, Ticker) # in our __init__.py file is _delete_record function, just does basic session.delete(obj) + commit()
        output_lines.append(
                f"Account successfully deleted for user {remote_number}!"
            )
        return _send_message(output_lines) # send a response
    
    # adds any amount of ticker to db
    if incoming_msg[0:3] == "add":
        stocks = incoming_msg.split()
        for ticker in stocks[1:]:
            ticker = ticker.upper()
            # Checks if the stock input is already in our db to avoid duplicates
            if not bool(Ticker.query.filter_by(tickers=ticker).first()):
                stockObj = Stock(ticker, token=os.getenv('IEX_TOKEN'))
                try:
                    stockObj.get_quote()['latestPrice']
                    add_stock = Ticker(user.phone_number, ticker)
                    _update_db(add_stock)
                    output_lines.append(
                        f"*{ticker}* stored successfully."
                        )
                except: 
                    output_lines.append(f'An error occured trying to add *{ticker.upper()}*.\nPerhaps a typo!')
            else:
                output_lines.append(
                    f"*{ticker}* previously stored."
                    )
        return _send_message(output_lines)


    # removes any amount of ticker given
    if incoming_msg[0:6] == "remove":
        stocks = incoming_msg.split()
        for ticker in stocks[1:]:
            ticker = ticker.upper()
            # Checks if ticker exists in db before deleting
            try:
                if bool(Ticker.query.filter_by(tickers=ticker).one()):
                    obj = Ticker.query.filter_by(tickers=ticker).one()
                    _delete_record(obj, None)
                    output_lines.append(f"*{ticker.upper()}* successfully removed.")
            except:
                output_lines.append(f"*{ticker.upper()}* not found in profile.")
        return _send_message(output_lines)
    
    if incoming_msg[0:4] == 'show':
        if not Ticker.query.all():
            output_lines.append('No tickers in profile! Please add a ticker.')
            return _send_message(output_lines)
        # Generator that 1st query searches a table
        # Then for each record inside our ticker column append to list
        all_tickers = [ticker.tickers for ticker in Ticker.query.all()]
        stockObj = Stock(all_tickers, token=os.getenv('IEX_TOKEN')) # an object holding a list
        # # stockObj is a Stock obj which obtained a list as a parameter
        # # So to access the particular index we must access via JSON-like key/value
        # # stockObj.get_quote()['TSLA']['latestPrice'] for example
        if len(all_tickers) > 1:
            for ticker in all_tickers:
                ticker = str(ticker)
                try:
                    output_lines.append('*' + ticker.upper() + "*: " + str(stockObj.get_quote()[ticker.upper()]['latestPrice']))
                except:
                    output_lines.append(f'An error occured for ticker: *{ticker.upper()}*.\nPerhaps a typo!')
        else:
            ticker = str(all_tickers[0])
            stockObj = Stock(ticker, token=os.getenv('IEX_TOKEN'))
            try:
                output_lines.append('*' + ticker.upper() + "*: " + str(stockObj.get_quote()['latestPrice']))
            except:
                output_lines.append(f'An error occured for ticker: *{ticker.upper()}*.\nPerhaps a typo!')
        return _send_message(output_lines)

    output_lines.append(f"Sorry, I didn't understand the command '{incoming_msg}', please try again or text 'help'.")
    return _send_message(output_lines)