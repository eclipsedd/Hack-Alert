from bs4 import BeautifulSoup
from datetime import datetime


def hack2skill_extractor(r_path, base_url):
    with open(r_path, "r", encoding="utf-8") as f:
        dat = f.read()
        soup = BeautifulSoup(dat, "html.parser")

    events_data = []

    event_blocks = soup.find_all("div", class_="swiper-slide newCard")

    for block in event_blocks:
        event = []

        name = block.find("h6").get_text(strip=True)
        event.append(name)

        description = block.find("p", class_="hack-description").get_text(strip=True)
        event.append(description)

        last_date = (
            block.find("p", class_="last-date")
            .get_text(strip=True)
            .replace("Last date to register:", "")
            .strip()
        )
        try:
            last_date_obj = datetime.strptime(last_date, "%a %b %d %Y")
            if last_date_obj < datetime.now():
                continue
        except ValueError:
            continue

        event.append("Due date: " + last_date[-15:])

        mode_text = block.find("p", class_="hack-type").get_text(strip=True)
        mmode = str(mode_text).split(":")
        event.append(mmode[1])

        link = block.find("a", class_="text-link")["href"]
        event.append(link)

        events_data.append(event)

    return events_data


# html_path = "data/hack2skill.html"
# base_url = "https://vision.hack2skill.com"
# events = hack2skill_extractor(html_path, base_url)

# for i in events:
#     print(i[0])
#     print(i[1])
#     print(i[2])
#     print(i[3])
#     print(i[4])
#     print()
