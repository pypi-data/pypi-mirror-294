from io import IOBase
from typing import Any, Union
from dataclasses import dataclass

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

@dataclass
class SlackClient:

    token: str = ''
    channel: str = ''

    def _client(self):
        if self.token == '':
            raise TypeError("missing required parameter: slack robot token")
        return WebClient(self.token)

    def post(self, text: str=""):
        if self.channel == '':
            raise TypeError("missing required parameter: slack channel ID")
        try:
            response = self._client().chat_postMessage(channel=self.channel, text=text)
        except SlackApiError as e:
           print(f"Got an error: {e.response['error']}") 

    def upload(self, file: Union[str, bytes, IOBase, None], filename: Union[str, None]):
        if self.channel == '':
            raise TypeError("missing required parameter: slack channel ID")
        try:
            return self._client().files_upload_v2(channel=self.channel, file=file, filename=filename)
        except SlackApiError as e:
           print(f"Got an error: {e.response['error']}") 