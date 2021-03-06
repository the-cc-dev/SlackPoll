__author__ = 'jhroyal'

import traceback
import requests
from flask import Flask
from flask import request
import Poll

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def vote_command():
    if request.method == "GET":
        return "The voting machine is up and running."

    token = request.form["token"]
    requested = request.form["text"]

    print ("%s - %s:%s - %s" % (request.form["user_name"], request.form["channel_name"], request.form["channel_id"], request.form["text"]))

    if "register" in requested:
        command = requested.split(" ")
        slack_url = command[1]
        slack_token = command[2]
        result = Poll.register_slack_account(slack_url, slack_token)
        return result

    if not Poll.validate_token(token):
        return "This Slack Account hasn't been registered with the polling application.\n" \
               "Please run `/poll register [incoming webhook url] [slash command token]`"

    try:
        requested = request.form["text"]
        if "help" in requested:
            return "*Help for /poll*\n\n" \
                   "*Start a poll:* `/poll create [question] options [option1] --- [option2] --- [option3]`\n" \
                   "*End a poll:* `/poll close` (The original poll creator must run this)\n" \
                   "*Cast a Vote:* `/poll cast [option number]`\n" \
                   "*Get number of votes cast so far:* `/poll count`"

        if "create" in requested and "options" in requested:
            print "Creating a new poll"
            return Poll.create(token, request)

        elif "cast" in requested:
            print "Casting a vote"
            return Poll.cast(token, request)

        elif "count" in requested:
            print "Getting vote count"
            return Poll.count(token, request)

        elif "close" in requested:
            print "Closing a poll"
            return Poll.close(token, request)

        else:
            return "Unknown request recieved"
    except requests.exceptions.ReadTimeout:
        return "Request timed out :("
    except Exception as e:
        print traceback.format_exc()
        return "Oh no! Something went wrong!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
