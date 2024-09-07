from typing import Any
from dataclasses import dataclass, field

from .slack_client import SlackClient

@dataclass
class SlackMessage:

    client: SlackClient

    def post(self, text: str) -> None:
        self.client.post(text=text)
    
    def upload(self, file_path: str) -> None:
        self.client.upload(file=file_path, filename=file_path)