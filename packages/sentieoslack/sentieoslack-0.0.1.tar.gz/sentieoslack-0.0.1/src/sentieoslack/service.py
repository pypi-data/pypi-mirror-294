from typing import List

import warnings

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from .constants import STATUS_CODES
from .utility import SlackMessage, get_log_message


class SlackService:
    def __init__(self, token: str) -> None:
        self.client = WebClient(token=token)

    def post_message(self, channel: str, message: str = "") -> int:
        """
        :param channel: slack channel
        :param message: plain rich text to be sent on slack
        :return: status code
        """
        try:
            self.client.chat_postMessage(channel=channel, text=message)
            return STATUS_CODES["SUCCESS"]

        except SlackApiError:
            return STATUS_CODES["ERROR"]

    def send_logs_to_slack(
        self,
        message_dict: SlackMessage,
        channel: str,
        text: str = "No Preview",
    ) -> int:
        """
        :param message_dict: {title: "", text:"" , link: ""}
        :param channel: slack channel
        :param channel: text : preview message
        :return: status code
        """
        try:
            message = get_log_message(message_dict)
            self.client.chat_postMessage(
                channel=channel, attachments=message, text=text
            )
            return STATUS_CODES["SUCCESS"]

        except SlackApiError:
            return STATUS_CODES["ERROR"]

    def send_file_to_slack(
        self, channels: List[str], file_name: str, additional_message: str = ""
    ) -> int:
        """
        :param channels: list of comma separated channels
        :param file_name: file to be uploaded
        :param additional_message: optional : comment
        :return: status code
        """
        warnings.warn("Deprecated", DeprecationWarning)
        try:
            self.client.files_upload(
                channels=channels, file=file_name, initial_comment=additional_message
            )
            return STATUS_CODES["SUCCESS"]
        except SlackApiError:
            return STATUS_CODES["ERROR"]
