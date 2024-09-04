"""Utils to send alerts in Teams
"""

import json
import logging
import os

import requests

from mxq_data_science_db.settings.settings import Settings

settings = Settings()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class teamsAlert:
    WEBHOOK_ULR = os.environ.get("TEAMS_WEBHOOK_ULR")

    def __init__(self, script_name: str):
        """
        Args:
            script_name (str): script name
        """
        self.script_name = script_name
        if teamsAlert.WEBHOOK_ULR is None:
            self.get_secret()

    def get_secret(self):
        """Get webhook from secret manager"""
        teams_secrets = settings.get_aws_secrets("teams_secret")
        teamsAlert.WEBHOOK_ULR = teams_secrets.get("WEBHOOK_ULR")
        assert teamsAlert.WEBHOOK_ULR, "webhook not set"

    def _build_body(self, messages_list: list) -> list:
        """Build the body for the request

        Args:
            messages_list (list): list of messages
        Return
            body as a list
        """
        body = [
            {
                "type": "TextBlock",
                "text": f"AlertBot: **{self.script_name}**",
                "id": "Title",
                "spacing": "Medium",
                "size": "Medium",
                "weight": "Bolder",
            },
        ]
        body_messages = [
            {
                "type": "TextBlock",
                "text": msg,
                "id": f"acMsg{i}",
                "wrap": True,
            }
            for i,msg in enumerate(messages_list)
        ]
        body.extend(body_messages)
        return body

    def send_message(self, messages_list: list):
        """Send message to teams

        Args:
            messages_list (list): messages
        """
        body = self._build_body(messages_list)
        headers = {"Content-Type": "application/json", "charset": "UTF-8"}
        payload = {
            "type": "message",
            "attachments": [
                {
                    "contentType": "application/vnd.microsoft.card.adaptive",
                    "contentUrl": None,
                    "content": {
                        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                        "type": "AdaptiveCard",
                        "version": "1.2",
                        "body": body,
                    },
                }
            ],
        }

        response = requests.post(
            teamsAlert.WEBHOOK_ULR,
            data=json.dumps(payload),
            headers=headers,
        )
        return response

    def _add_message_list(self, message: str, messages_list: list):
        """ADd message to message list and send

        Args:
            message (str): message
            messages_list (list): message list
        """
        messages_send = [message]
        messages_send.extend(messages_list)
        self.send_message(messages_send)

    def success_message(self, messages_list: list = []):
        """Send default success message

        Args:
            messages_list(list) : list of messages to be add to the alert
        """
        message = f"🟢 **{self.script_name}** ran successfully"
        self._add_message_list(message, messages_list)

    def error_message(self: str, messages_list: list = []):
        """Send default error message

        Args:
            messages_list(list) : list of messages to be add to the alert
        """
        message = f"🔴 Error running **{self.script_name}**"
        self._add_message_list(message, messages_list)

    def alert_message(self, messages_list: list = []):
        """Send default alert message

        Args:
            messages_list(list) : list of messages to be add to the alert
        """
        message = f"🟡 Alert in **{self.script_name}**"
        self._add_message_list(message, messages_list)
    
    def release_message(self, messages_list: list = []):
        """Send default alert message

        Args:
            messages_list(list) : list of messages to be add to the alert
        """
        message = f"🚀 New release **{self.script_name}**"
        self._add_message_list(message, messages_list)
