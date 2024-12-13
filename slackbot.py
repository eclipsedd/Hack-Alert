import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
from fetch import loader
from hacker_earth import hacker_earth_extractor

load_dotenv()

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

client = WebClient(token=SLACK_BOT_TOKEN)

hackathon_sites = {
    "hacker_earth": "https://www.hackerearth.com/challenges/?filters=competitive%2Chackathon%2Cuniversity",
}

last_sent_event = "Certified Hedera Developer"


def save_html():
    for name, url in hackathon_sites.items():
        path = f"data/{name}.html"
        loader(url, path)


def send_message(event):
    message = f"{event[0]}\n" + f"{event[1]}\n" + f"{event[2]}\n" + f"{event[3]}"

    try:
        client.chat_postMessage(channel=CHANNEL_ID, text=message)
        print(f"Message sent.")
    except SlackApiError as e:
        print(f"Error sending message: {e.response['error']}")


def hacker_earth_scraper():
    mydat = hacker_earth_extractor(
        "data/hacker_earth.html", "https://www.hackerearth.com"
    )
    # print(mydat)
    return mydat


if __name__ == "__main__":
    # save_html()

    events = hacker_earth_scraper()
    # print(events)

    start_index = len(events)
    for i in range(len(events) - 1, -1, -1):
        if events[i][0] == last_sent_event:
            start_index = i
            break

    for i in range(0, start_index, 1):
        send_message(events[i])
        last_sent_event = events[i][0]

