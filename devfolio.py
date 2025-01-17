from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import platform
import os


def devfolio_extractor():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")

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
    driver.get("https://devfolio.co/hackathons/open")

    try:
        WebDriverWait(driver, 40).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div[class*='CompactHackathonCard__StyledCard']"),
            )
        )

        cards = driver.find_elements(
            By.CSS_SELECTOR, "div[class*='CompactHackathonCard__StyledCard']"
        )

        hackathon_data = []

        for card in cards:
            name_element = card.find_element(By.TAG_NAME, "h3")
            name = name_element.text.strip()

            link_element = name_element.find_element(By.XPATH, "./ancestor::a")
            link = link_element.get_attribute("href")

            theme = card.find_element(
                By.XPATH, ".//p[text()='Theme']/following-sibling::div//p"
            ).text.strip()

            mode = card.find_element(
                By.XPATH,
                ".//p[contains(@class, 'cqgLqK') and text()='Online' or text()='Offline']",
            ).text.strip()

            start_date = card.find_element(
                By.XPATH, ".//p[contains(text(), 'Starts')]"
            ).text

            hackathon_data.append(
                [
                    "*" + name + "*",
                    "*Theme:* " + theme,
                    "*Starts:* " + start_date[-8:],
                    "*Mode:* " + mode,
                    link,
                ]
            )

        return hackathon_data

    except TimeoutException:
        return []
    except Exception as e:
        return []
    finally:
        driver.quit()


# hackathons = devfolio_extractor()
# print(f"\nNo. of hackathons: {len(hackathons)}")
# for i in hackathons:
#     print(i[0])
#     print(i[1])
#     print(i[2])
#     print(i[3])
#     print(i[4])
#     print()
