from bs4 import BeautifulSoup
import re
from datetime import timedelta


def myextractor(r_path, base_url):
    with open(r_path, "r") as f:
        dat = f.read()
        soup = BeautifulSoup(dat, "html.parser")

    event_containers = soup.find_all("div", class_="challenge-card-modern")
    events_data = []

    for event in event_containers:
        # event name
        event_name_tag = event.find("span", class_="challenge-list-title")
        if event_name_tag:
            event_name = event_name_tag.text.strip()
        else:
            continue

        # event type
        event_type_tag = event.find(
            "div", class_="challenge-type light smaller caps weight-600"
        )
        if event_type_tag:
            event_type = event_type_tag.text.strip()
        else:
            event_type = "Unknown Type"

        # event link
        event_link_tag = event.find(
            "a", class_="challenge-card-wrapper challenge-card-link", href=True
        )
        if event_link_tag:
            href = event_link_tag["href"]
            event_link = href if href.startswith("https") else base_url + href
        else:
            event_link = "No Link"

        # extract the seconds_left value from <script>
        script_tag = event.find_next("script", type="text/javascript")
        seconds_left = 0
        if script_tag and script_tag.string:
            script_content = script_tag.string
            match = re.search(
                r"var\s+seconds_left\s*=\s*(\d+)\s*-\s*(\d+);", script_content
            )
            if match:
                event_end_time = int(match.group(1))
                current_time = int(match.group(2))
                seconds_left = event_end_time - current_time

        if seconds_left:
            remaining_time = str(timedelta(seconds=seconds_left))
        else:
            start_time_tag = event.find("div", class_="date less-margin dark")
            if start_time_tag:
                start_time = start_time_tag.text.strip()
                remaining_time = f"Starts on: {start_time}"
            else:
                remaining_time = "No Time Info"

        events_data.append([event_name, event_type, event_link, remaining_time])

    return events_data


base_url = "https://www.hackerearth.com"
mydat = myextractor("data.html", base_url)

# for i in mydat:
#     print(i[0])
#     print(i[1])
#     print(i[2])
#     print(i[3])
#     print()

"""
data format-> nested lists of strings
Analog Kairos Hackathon - 2
HACKATHON
https://analog-part2.hackerearth.com/
31 days, 16:37:37

Global Scholar Challenge
COMPETITIVE
https://www.hackerearth.com/challenges/competitive/global-scholar-challenge/
Starts on: Dec 20, 12:30 PM UTC (UTC)
"""
