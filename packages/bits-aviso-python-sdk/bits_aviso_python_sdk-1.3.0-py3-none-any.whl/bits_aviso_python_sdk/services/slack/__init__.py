import json
import logging
import requests
from bits_aviso_python_sdk.services.google.secretmanager import SecretManager
from bits_aviso_python_sdk.services.slack import payload_builder


class Slack:
    def __init__(self, gcp_webhook=(None, None, None), webhook_url=None):
        """Initializes the Slack class. If GCP webhook is provided, it will be used to get the webhook url from
        secret manager using the default google credentials.

        Args:
            gcp_webhook (tuple, optional): A tuple containing the GCP project, secret name, and secret version.
                Defaults to (None, None, None).
            webhook_url (str, optional): The webhook url to use. Defaults to None.

        Raises:
            ValueError: If GCP webhook or webhook url is not provided.
        """
        if webhook_url:
            self._webhook_url = webhook_url

        elif gcp_webhook:
            self._set_webhook_url_from_gcp(gcp_webhook)

        else:
            raise ValueError('Either GCP webhook or webhook url must be provided.')

    def _set_webhook_url_from_gcp(self, gcp_webhook):
        """Gets the webhook url from secret manager and sets it to _webhook_url.

        Args:
            gcp_webhook (tuple): A tuple containing the GCP project, secret name, and secret version.
        """
        secret_manager = SecretManager()
        self._webhook_url = secret_manager.get_secret(gcp_webhook[0], gcp_webhook[1], gcp_webhook[2])

    def post(self, payload):
        """Post a message to Slack using the payload data.

        Args:
            payload (dict): The payload to send to Slack.

        Returns:
            bool: True if the message was posted successfully, False otherwise.
        """
        try:
            response = requests.post(
                self._webhook_url,
                data=json.dumps(payload),
                headers={'Content-Type': 'application/json'}
            )
            response.raise_for_status()
            logging.info('Message posted to Slack')
            return True

        except requests.exceptions.HTTPError as err:
            logging.error(f'Error posting message to Slack: {err}')
            return False

    def post_basic_alert(self, data):
        """Post a basic alert to Slack using the data.
        The data dict should contain the keys in the example below:
        data = {
            "project": "project-name",
            "service_name": "service-name",
            "logging_level": "logging-level",
            "message": "message"
        }

        Args:
            data (dict): The data to use to build the basic alert.

        Returns:
            bool: True if the message was posted successfully, False otherwise.
        """
        try:
            payload = payload_builder.basic_alert(data)  # build payload with given data
            success = self.post(payload)  # post the payload to slack

            if success:
                return True
            else:
                raise ValueError('Failed to post basic alert to Slack.')

        except ValueError as e:
            logging.error(f'Error building payload for basic alert: {e}')
            return False

    def post_cloud_function_alert(self, data):
        """Post a cloud function alert to Slack using the data.
        The data dict should contain the keys in the example below:
        data = {
            "project_id": "project_id",
            "function_name": "function_name",
            "logging_level": "logging_level",
            "message": "message"
        }

        Args:
            data (dict): The data to use to build the cloud function alert.

        Returns:
            bool: True if the message was posted successfully, False otherwise.
        """
        try:
            payload = payload_builder.cloud_function(data)  # build payload with given data
            success = self.post(payload)  # post the payload to slack

            # verify if the message was posted successfully
            if success:
                return True
            else:
                raise ValueError('Failed to post cloud function alert to Slack.')

        except ValueError as e:
            logging.error(f'Error building payload for cloud function alert: {e}')
            return False
