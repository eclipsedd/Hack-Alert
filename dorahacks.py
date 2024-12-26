from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time


def dorahacks_extractor():
    driver = webdriver.Chrome()

    try:
        driver.get("https://dorahacks.io/hackathon")
        driver.maximize_window()

        time.sleep(10)
        driver.execute_script("window.scrollBy(0, 400);")

        sort_button = driver.find_element(By.XPATH, "//button[span[text()='Sort']]")
        sort_button.click()

        time.sleep(1)

        recently_added = driver.find_element(By.XPATH, "//div[text()='Recently Added']")
        recently_added.click()

        time.sleep(5)

        hackathon_data = []

        hackathon_cards = driver.find_elements(
            By.XPATH, "//ul[contains(@class, 'hackathon-list')]/li"
        )

        for card in hackathon_cards:
            try:
                status = card.find_element(
                    By.XPATH, ".//span[@aria-label='hackathon-status']"
                ).text
                if status == "Ended":
                    continue

                link = card.find_element(By.XPATH, ".//a").get_attribute("href")

                name = card.find_element(
                    By.XPATH, ".//span[@class='font-semibold line-clamp-2']"
                ).text

                organiser = card.find_element(
                    By.XPATH,
                    ".//span[contains(@class, 'text-ink-secondary') and not(@aria-label)]",
                ).text

                mode = card.find_element(
                    By.XPATH,
                    ".//div[contains(@class, 'flex flex-row gap-x-1 items-center')]/span",
                ).text

                tags_elements = card.find_elements(
                    By.XPATH,
                    ".//div[@class='inline-block text-accent-primary bg-accent-bg text-xs px-1 py-0.5 rounded me-2']",
                )
                tags = ", ".join([tag.text for tag in tags_elements])

                prize_pool = card.find_element(
                    By.XPATH,
                    ".//span[contains(@class, 'text-lg font-semibold text-accent-primary')]",
                ).text

                hackathon_data.append(
                    [
                        name,
                        organiser,
                        mode,
                        tags,
                        prize_pool,
                        status,
                        link,
                    ]
                )

            except Exception as e:
                print(f"Error extracting data for a card: {e}")
                continue

        return hackathon_data

    finally:
        driver.quit()


# events = dorahacks_extractor()
# print(f"Number of hackathons: {len(events)}")
# for i in events:
#     print("Name:", i[0])
#     print("Organiser:", i[1])
#     print("Mode:", i[2])
#     print("Tags:", i[3])
#     print("Prize Pool:", i[4])
#     print("Status:", i[5])
#     print("Link:", i[6])
#     print()
