import logging


from flask import request, render_template
from bot import app
from bot.logic.logic import Logic

logic = Logic()


@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 404


@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    logging.debug(data)

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                logic.parse_messaging_event(messaging_event)
    return "ok", 200


@app.route('/database', methods=['GET'])
def database():
    users = logic.get_all_users()
    return render_template('database.html', users=users)
