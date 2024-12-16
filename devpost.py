from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time


def devpost_extractor():
    driver = webdriver.Chrome()
    driver.get(
        "https://devpost.com/hackathons?open_to[]=public&order_by=recently-added&status[]=upcoming&status[]=open"
    )

    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        for i in range(last_height - 2000, last_height, 1000):
            driver.execute_script(f"window.scrollTo(0, {i});")
            time.sleep(0.5)

        time.sleep(1)

        try:
            end_message = driver.find_element(By.CSS_SELECTOR, "p.faded").text
            if "End of results" in end_message:
                break
        except NoSuchElementException:
            pass

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    cat = [
        "div.hackathon-tile.clearfix.open.mb-5",
        "div.hackathon-tile.clearfix.upcoming.mb-5",
        "div.hackathon-tile.clearfix.open.featured.mb-5",
    ]
    events = []
    for i in cat:
        elems = driver.find_elements(By.CSS_SELECTOR, i)
        for elem in elems:
            try:
                link = elem.find_element(
                    By.CSS_SELECTOR, "a.flex-row.tile-anchor"
                ).get_attribute("href")
                title = elem.find_element(By.CSS_SELECTOR, "h3").text
                status = (
                    "status: "
                    + elem.find_element(
                        By.CSS_SELECTOR, "div.round.label.status-label"
                    ).text
                )

                mode = (
                    "mode: " + elem.find_element(By.CSS_SELECTOR, "div.info span").text
                )

                host_name = (
                    "host: "
                    + elem.find_element(By.CSS_SELECTOR, "span.host-label").text
                )

                duration = (
                    "dates: "
                    + elem.find_element(By.CSS_SELECTOR, "div.submission-period").text
                )

                themes = elem.find_elements(By.CSS_SELECTOR, "span.theme-label")
                theme = ""
                for i in themes:
                    theme += ", " + i.text
                theme = "themes: " + theme[1:]

                event = [
                    title,
                    mode,
                    status,
                    theme,
                    host_name,
                    duration,
                    link,
                ]
                events.append(event)

            except Exception as e:
                pass

    driver.quit()
    return events


# mydat = devpost_extractor()
# print(len(mydat))

# for i in mydat:
#     print(i[0])
#     print(i[1])
#     print(i[2])
#     print(i[3])
#     print(i[4])
#     print(i[5])
#     print(i[6])