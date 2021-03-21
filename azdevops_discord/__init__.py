from flask import Flask, request, Response

from . import events

import logging
import requests
import os

loglevel = {
    'CRITICAL': logging.CRITICAL,
    'ERROR': logging.ERROR,
    'WARNING': logging.WARNING,
    'INFO': logging.INFO,
    'DEBUG': logging.DEBUG,
}

logging.basicConfig(level=loglevel[os.environ.get('LOG_LEVEL', 'INFO')])
app = Flask(__name__)

eventBindings = {
    'build.complete': events.build_complete,
    'git.pullrequest.created': events.git_pullrequest_created
}


def send_discord_embed(embed: dict):
    discord = os.environ["DISCORD_WEBHOOK"]
    body = {
        'username': 'Azure DevOps',
        'avatar_url': 'https://pbs.twimg.com/profile_images/1145617831905681408/XNKktHjN_400x400.png',
        'embeds': [
            embed
        ]
    }

    r = requests.post(
        discord,
        json=body
    )

    return r.text, r.status_code

    

@app.route('/', methods=['POST'])
def handle():
    ip_address = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    app.logger.info(f"Request from {ip_address}")

    try:
        event = request.json['eventType']
        app.logger.info(f"Event: {event}")
        event_handler = eventBindings[event]
    except Exception as e:
        return f"{e} is not a valid event", 500

    error, embed = event_handler(request.json)

    if error:
        return str(error), 500

    return send_discord_embed(embed)


if __name__ == '__main__':
    app.run()