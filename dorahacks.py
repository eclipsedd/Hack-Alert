from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import platform
import os


def dorahacks_extractor():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    )

    if platform.system() == "Windows":
        service = Service(ChromeDriverManager().install())
    else:
        # linux env
        options.binary_location = os.getenv(
            "CHROME_BINARY_LOCATION", "/opt/google/chrome/chrome"
        )
        service = Service(
            executable_path=os.getenv("CHROMEDRIVER_PATH", "/usr/bin/chromedriver")
        )

    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get("https://dorahacks.io/hackathon")
        driver.maximize_window()

        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.XPATH, "//ul[contains(@class, 'hackathon-list')]")
            )
        )

        driver.execute_script("window.scrollBy(0, 400);")

        sort_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Sort']]"))
        )
        sort_button.click()

        recently_added = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//div[text()='Recently Added']"))
        )
        recently_added.click()

        WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//ul[contains(@class, 'hackathon-list')]/li")
            )
        )

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
                # print(f"Error extracting data for a card: {e}")
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
