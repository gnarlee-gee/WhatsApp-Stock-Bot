from flask import request
from app import app, _update_db
from app.models import User, Flashcard
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
    # incoming From is "whatsapp:'phonenum'"
    if remote_number.startswith("whatsapp:"):
        remote_number = remote_number.split(":")[1]

    user = User.query.get(remote_number)

    # Commands available
    if incoming_msg == "commands":
        output_lines.append("'create' - creates a new account")
        output_lines.append(
            "'add' - start the process of adding tickers to account")
        output_lines.append(
            "'show' - Shows current market price for users tickers")
        output_lines.append(
            "'delete ticker' - start the process of deleting ticker(s) from account")
        output_lines.append("'delete account' - delete your account")
        return _send_message(output_lines)

    if not user:
        if incoming_msg == "create":
            new_user = User(remote_number)
            _update_db(new_user)
            output_lines.append(
                f"Account successfully created for number {remote_number}!"
            )
            output_lines.append(
                "To get started, text 'add' to start inserting tickers to your account."
            )
            output_lines.append(
                "When you're finished, text 'stop adding'."
            )
            output_lines.append(
                "You can text 'show' to show the market price of your stock(s)."
            )
            output_lines.append(
                "Text 'commands' at any time to see available commands."
            )
        else:
            output_lines.append(
                "Please register with 'create', first!")

        return _send_message(output_lines)
    else:
        if incoming_msg == "create":
            output_lines.append(
                f"You have already registered {remote_number}. Text 'command' for available options.")
            return _send_message(output_lines)
