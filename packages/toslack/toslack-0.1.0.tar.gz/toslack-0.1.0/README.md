<h1 align="center">Python API and CLI for sending message in Slack</h1>

<p align="center">
    <a href="https://pypi.org/project/toslack/">
        <img alt="PyPI - Version" src="https://img.shields.io/pypi/v/toslack"></a>
    <a href="https://pypi.org/project/slack-sdk/">
        <img alt="slack-to Versions" src="https://img.shields.io/badge/slack--sdk-%3E%3D3.31.0-red"></a>
    <a href="https://pypi.org/project/toslack/">
        <img alt="Python Versions" src="https://img.shields.io/pypi/pyversions/toslack.svg"></a>
</p>

**toslack** is a Python package that helps you send messages, images or files to slack channels with simple settings. Command line tools are also provided to do the same thing.

### Requirements

- **Python Version**: Ensure you are using Python 3.6 or higher.
- **Dependencies**:
  - `slack_sdk` (version 3.31.0)
  - `dataclasses` (built-in for Python 3.6+)
  - `typing` (for type hinting)

## Installation

```
pip install toslack
```

## Sending a message to Slack

One of the most common use-cases is sending a message to Slack. If your app's bot user is not in a channel yet, invite the bot user before running the code snippet (or add `chat:write.public` to Bot Token Scopes for posting in any public channels).

```
import os
from toslack import SlackMessage
from toslack import SlackClient

client = SlackClient(token=os.environ['SLACK_BOT_TOKEN'], channel=os.environ['TO_SLACK_CHANNEL'])
message = SlackMessage(client=client)
message.post(text="Hello world!")
```

Or posting your message by the command line.

```
python slack.py --token xxx --channel C123456 post $message
```

## Uploading files to Slack

You can just include a path to the file directly in the API call and upload it that way.

```
import os
from toslack import SlackMessage
from toslack import SlackClient

client = SlackClient(token=os.environ['SLACK_BOT_TOKEN'], channel=os.environ['TO_SLACK_CHANNEL'])
message = SlackMessage(client=client)
message.upload(file_path="./tmp.txt")
```

Or upload by specifying the file path on the command line.

```
python slack.py --token xxx --channel C123456 upload $file_path
```