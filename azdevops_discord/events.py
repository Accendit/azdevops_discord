
def git_pullrequest_created(event_body: dict) -> (Exception, dict):
    try:
        embed = {
            'title': f"Pull Request #{event_body['resource']['pullRequestId']} {event_body['resource']['title']}",
            'url': event_body['resource']['url'],
            'description': event_body['resource']['description'],
            'author': {
                'name': event_body['resource']['createdBy']['displayName'],
                'icon_url': event_body['resource']['createdBy']['imageUrl'],
                'url': event_body['resource']['createdBy']['url']
            },
            'footer': {
                'text': f"Status: {event_body['resource']['status']}, Merge: {event_body['resource']['mergeStatus']}"
            }
        }
        return None, embed
    except KeyError as e:
        return e, None


def build_complete(event_body: object) -> (Exception, dict):
    try:
        embed = {
            'title': f"Build {event_body['resource']['buildNumber']} {event_body['resource']['status']}",
            'url': event_body['resource']['url'],
            'description': f"Last changed by {event_body['resource']['lastChangedBy']['displayName']}",
        }
        return None, embed
    except KeyError as e:
        return e, None