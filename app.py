from flask import Flask, request, Response
import requests
import os

app = Flask(__name__)

def process_pr(devops_body: object):
    discord = os.environ["DISCORD_WEBHOOK"]
    body = {
        'username': 'Azure DevOps',
        'avatar_url': 'https://pbs.twimg.com/profile_images/1145617831905681408/XNKktHjN_400x400.png',
        'embeds': [
            {
                'title': f"Pull Request #{devops_body['resource']['pullRequestId']} {devops_body['resource']['title']}",
                'url': devops_body['resource']['url'],
                'description': devops_body['resource']['description'],
                'author': {
                    'name': devops_body['resource']['createdBy']['displayName'],
                    'icon_url': devops_body['resource']['createdBy']['imageUrl'],
                    'url': devops_body['resource']['createdBy']['url']
                },
                'footer': {
                    'text': f"Status: {devops_body['resource']['status']}, Merge: {devops_body['resource']['mergeStatus']}"
                }
            }
        ]
    }

    r = requests.post(
        url=discord,
        json=body
    )

    return r.text, r.status_code
    
    

@app.route('/', methods=['POST'])
def handle():
    ip_address = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    app.logger.debug(f"Request from {ip_address}")

    if not request.is_json:
        app.logger.error("Unable to parse JSON")
        return "Unable to parse JSON", 500

    return process_pr(request.json)

    return Response(status=200)

if __name__ == '__main__':
    app.run()