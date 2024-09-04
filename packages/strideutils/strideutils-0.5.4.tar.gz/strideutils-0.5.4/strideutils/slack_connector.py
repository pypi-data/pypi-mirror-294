import os
import traceback
from typing import List, Optional, Union

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from strideutils.stride_config import config


def post_msg(
    txt: Union[str, List[str]],
    channel: str,
    token: str = config.STRIDEBOT_API_TOKEN,
    botname: Optional[str] = None,
    unfurl_links: bool = False,
    unfurl_media: bool = False,
    thread_ts: Optional[str] = None,
):
    """
    Posts a slack message to the given channel, e.g.

        post_msg('hello world', 'general')

    if txt is an array, this will post each element of the array as a thread

    Args:
      username: Rename stridebot
    """
    client = WebClient(token=token)
    channel = config.slack_channels.get(channel.replace('#', ''), channel)
    channel = os.environ.get('SLACK_CHANNEL_OVERRIDE', default=channel)

    # Listify
    messages = [txt] if type(txt) is str else txt

    # thread ts keeps track of the latest thread ID so we can keep replying in-thread
    thread_ts = None or thread_ts
    for msg in messages:
        try:
            response = client.chat_postMessage(
                channel=channel,
                text=msg,
                thread_ts=thread_ts,
                username=botname,
                unfurl_links=unfurl_links,
                unfurl_media=unfurl_media,
            )
            if thread_ts is None:  # API advises to use parent IDs instead of child's
                thread_ts = response['ts']
        except SlackApiError as e:
            print("Error sending message: ", e)
            raise
    return thread_ts


def upload_file(file_name: str, content: str) -> str:
    '''
    This uploads a file called "file_name" with the string contents "content"

    This will return a link that can be used to embed a file in slack.
    For example:
        url = upload_file("test.txt", "Hello World")
        post_msg(f"<{url}|This is a file>", channel="#alerts-debug")
    '''
    client = WebClient(token=config.STRIDEBOT_API_TOKEN)
    try:
        slack_file = client.files_upload_v2(filename=file_name, content=content)
    except Exception as e:
        print(f"Error uploading file to slack: {e}")
        traceback.print_exc()
        raise ValueError(f"Error uploading file to slack: {e}")
    file_link = slack_file['file']['permalink']
    return file_link
