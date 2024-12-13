import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
from fetch import loader
from hacker_earth import hacker_earth_extractor
from hack2skill import hack2skill_extractor
import schedule
import time
import json


load_dotenv()

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

client = WebClient(token=SLACK_BOT_TOKEN)

hackathon_sites = {
    "hacker_earth": "https://www.hackerearth.com/challenges/?filters=competitive%2Chackathon%2Cuniversity",
    "hack2skill": "https://hack2skill.com/#ongoin-initiatives",
}

STATE_FILE = "last_sent_event.json"

if os.path.exists(STATE_FILE):
    with open(STATE_FILE, "r") as f:
        last_sent_event = json.load(f)
else:
    last_sent_event = [" "] * len(hackathon_sites)


def save_last_sent_event():
    with open(STATE_FILE, "w") as f:
        json.dump(last_sent_event, f)


def save_html():
    for name, url in hackathon_sites.items():
        path = f"data/{name}.html"
        loader(url, path)


def send_message(event):
    message = ""
    for i in range(len(event)):
        message += f"{event[i]}\n"

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


def hack2skill_scraper():
    mydat = hack2skill_extractor(
        "data/hack2skill.html", "https://vision.hack2skill.com"
    )
    # print(mydat)
    return mydat


def myfunc(events, index):
    start_index = len(events)
    for i in range(len(events) - 1, -1, -1):
        if events[i][0] == last_sent_event[index]:
            start_index = i
            break

    for i in range(start_index - 1, -1, -1):
        send_message(events[i])
        last_sent_event[index] = events[i][0]

    save_last_sent_event()


def main():
    save_html()

    events = hacker_earth_scraper()
    myfunc(events, 0)

    events = hack2skill_scraper()
    myfunc(events, 1)
    print("executed")


schedule.every(30).minutes.do(main)

if __name__ == "__main__":
    main()
    while True:
        schedule.run_pending()
        time.sleep(1)
