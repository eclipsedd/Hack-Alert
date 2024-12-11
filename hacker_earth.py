from bs4 import BeautifulSoup


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

        # event link
        event_link_tag = event.find(
            "a", class_="challenge-card-wrapper challenge-card-link", href=True
        )
        if event_link_tag:
            href = event_link_tag["href"]
            event_link = href if href.startswith("https") else base_url + href
        else:
            event_link = "No Link"

        events_data.append([event_name, event_link])

    return events_data


base_url = "https://www.hackerearth.com"
mydat = myextractor("data.html", base_url)

# for i in mydat:
#     print(i[0])
#     print(i[1])
#     print()
