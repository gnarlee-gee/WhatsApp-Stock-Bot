from flask import request
from app import app, _update_db, _delete_record
from app.models import User
from twilio.twiml.messaging_response import MessagingResponse


def _send_message(output_lines):
    resp = MessagingResponse()
    msg = resp.message()
    msg.body("\n".join(output_lines))
    return str(resp)


@app.route("/bot", methods=["POST"])
def bot():
    incoming_msg = request.values.get("Body", "").strip().lower()
    remote_number = request.values.get("From", "")
    output_lines = []
    # incoming From is "whatsapp:#######"
    if remote_number.startswith("whatsapp:"):
        remote_number = remote_number.split(":")[1]

    #TODO: CREATE A RANDOM NUMBER TO ASSIGN!
    if not remote_number:
        remote_number = "123"

    user = User.query.get(remote_number)

    # Help commands
    # - 'help'
    if incoming_msg == "help":
        output_lines.append("'create' - create a new account")
        output_lines.append("'add ticker1 ticker2 ... tickerN' - adds any amount of tickers to your account")
        output_lines.append("'remove ticker1 ticker2 ... tickerN' - removes selected tickers from account")
        output_lines.append("'show' - displays market prices of stocks in your portfolio")
        output_lines.append("'delete account' - deletes account")
        output_lines.append("***DO NOT INCLUDE ' ' in your commands!***")
        return _send_message(output_lines)

    # User creation commands
    # - 'create account'
    if not user:
        if incoming_msg == "create":
            new_user = User(remote_number)
            _update_db(new_user)
            output_lines.append(
                f"Account successfully created for number {remote_number}!"
            )
            output_lines.append(
                "To get started, text 'add ticker1 ticker2 ... tickerN' to start creating your portfolio."
            )
            output_lines.append(
                "You can text 'show' to see market prices of stocks in your portfolio."
            )
            output_lines.append(
                "Text 'help' at any time to see available commands."
            )
        else:
            output_lines.append("Please register with 'create account', first!")

        return _send_message(output_lines)
    else:
        if incoming_msg == "create":
            output_lines.append(f"You have already registered {remote_number}. Begin typing some commands!\nType 'help' for commands!.")
            return _send_message(output_lines)

    if incoming_msg == "delete":
        _delete_record(user)
        output_lines.append(
                f"Account successfully deleted for number {remote_number}!"
            )
        return _send_message(output_lines)
    
    
    
    # if not user.creating_flashcards and incoming_msg == "create flashcards":
    #     output_lines.append(
    #         "Create a new flashcard by texting in the form {front} / {back}."
    #     )
    #     output_lines.append(
    #         "For example 'hello / 你好' would create 'hello' on the front and '你好' on the back."
    #     )
    #     _update_db(user)
    #     return _send_message(output_lines)


    output_lines.append("Sorry, I don't understand, please try again or text 'help'.")
    return _send_message(output_lines)