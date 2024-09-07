from datetime import datetime


def basic_alert(data):
    """Creates the payload for the slack alert with the given data.
    The data dict should contain the keys in the example below:
    data = {
        "project": "project-name",
        "service_name": "service-name",
        "logging_level": "logging-level",
        "message": "message"
    }

    Args:
        data (dict): The data to be included in the slack alert.

    Returns:
        dict: The payload for the slack alert.

    Raises:
        ValueError: If the data dict does not contain the required keys.
    """
    # check if the data dict contains the required keys
    if not all(key in data for key in ["project", "service_name", "logging_level", "message"]):
        raise ValueError("The data dict must contain the keys: project, service_name, logging_level, message.")

    payload = {
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f":siren:  {data['project']} ALERT"
                }
            },
            {
                "type": "context",
                "elements": [
                    {
                        "text": f"*{datetime.now().strftime('%B %d, %Y')}*  |  Severity Level: {data['logging_level']}",
                        "type": "mrkdwn"
                    }
                ]
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f" :code: *{data['service_name']}*"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": data['message']
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": "bottom text"
                    }
                ]
            }
        ]
    }

    return payload


def cloud_function(data):
    """Creates the payload for the slack alert with the given data for a cloud function.
    The data dict should contain the keys in the example below:
    data = {
        "project_id": "project_id",
        "function_name": "function_name",
        "logging_level": "logging_level",
        "message": "message"
    }

    Args:
        data (dict): The data to be included in the slack alert.

    Returns:
        dict: The payload for the slack alert.

    Raises:
        ValueError: If the data dict does not contain the required keys.
    """
    # check if the data dict contains the required keys
    if not all(key in data for key in ["project_id", "function_name", "logging_level", "message"]):
        raise ValueError("The data dict must contain the keys: project_id, function_name, logging_level, message.")

    # proceed
    payload = {
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f":siren:  {data['project_id']} ALERT"
                }
            },
            {
                "type": "context",
                "elements": [
                    {
                        "text": f"*{datetime.now().strftime('%B %d, %Y')}*  |  Severity Level: {data['logging_level']}",
                        "type": "mrkdwn"
                    }
                ]
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f" :cloud: {data['function_name']}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": data['message']
                },
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Go to Logs",
                        # "emoji": True
                    },
                    "value": "click_me_123",
                    "url": f"https://console.cloud.google.com/functions/details/us-east4/"
                           f"{data['function_name']}?env=gen2&hl=en&{data['project_id']}&tab=logs",
                    "action_id": "button-action"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": "bottom text"
                    }
                ]
            }
        ]
    }
    return payload
