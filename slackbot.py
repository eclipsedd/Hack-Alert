import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
from fetch import loader
from hacker_earth import hacker_earth_extractor
from hack2skill import hack2skill_extractor
from devpost import devpost_extractor
from devfolio import devfolio_extractor
from dorahacks import dorahacks_extractor
from datetime import datetime, timedelta
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
DEVPOST_TRACKING_FILE = "devpost_sent.json"

if os.path.exists(STATE_FILE):
    with open(STATE_FILE, "r") as f:
        last_sent_event = json.load(f)
else:
    last_sent_event = [""] * 4


def save_last_sent_event():
    with open(STATE_FILE, "w") as f:
        json.dump(last_sent_event, f)


def load_devpost():
    try:
        with open(DEVPOST_TRACKING_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_devpost(tracked_events):
    with open(DEVPOST_TRACKING_FILE, "w") as file:
        json.dump(tracked_events, file, indent=4)


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


def devpost_send():
    events = devpost_extractor()
    tracked_events = load_devpost()

    new_events = []
    for event in events:
        title, duration = event[0], event[5][7:]
        if title in tracked_events and tracked_events[title] == duration:
            continue
        new_events.append(event)

    for i in new_events:
        send_message(i)

    # Removing outdated events, which expired more than a week ago
    updated_tracked_events = {}
    for title, duration in tracked_events.items():
        try:
            if " - " in duration:
                end_date_str = duration.split(" - ")[1]
            else:
                end_date_str = duration
            if len(end_date_str) < 11:
                end_date_str = duration.split(" - ")[0][:4] + end_date_str

            end_date = datetime.strptime(end_date_str, "%b %d, %Y")
            if datetime.now() <= end_date + timedelta(weeks=1):
                updated_tracked_events[title] = duration
        except Exception:
            continue

    for i in new_events:
        updated_tracked_events[i[0]] = i[5][7:]
    save_devpost(updated_tracked_events)


def main():
    save_html()

    events = hacker_earth_scraper()
    myfunc(events, 0)

    events = hack2skill_scraper()
    myfunc(events, 1)

    devpost_send()

    events = devfolio_extractor()
    myfunc(events, 2)

    events = dorahacks_extractor()
    myfunc(events, 3)

    print("executed")


schedule.every(60).minutes.do(main)

if __name__ == "__main__":
    main()
    while True:
        schedule.run_pending()
        time.sleep(1)
