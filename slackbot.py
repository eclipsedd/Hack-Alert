import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv

load_dotenv()

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

client = WebClient(token=SLACK_BOT_TOKEN)


def myfunc():
    return 0


def send_message(message):
    try:
        client.chat_postMessage(channel=CHANNEL_ID, text=message)
        print("Message sent")
    except SlackApiError as e:
        print(f"Error sending message: {e.response['error']}")


if __name__ == "__main__":
    result = myfunc()
    message = f"The result of the calculation is: {result}"
    send_message(message)
