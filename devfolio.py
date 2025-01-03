from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC


def devfolio_extractor():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")

    driver = webdriver.Chrome(options=options)
    driver.get("https://devfolio.co/hackathons/open")

    try:
        WebDriverWait(driver, 10).until(
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

            hackathon_data.append([name, link])

        return hackathon_data

    except TimeoutException:
        return []
    except Exception as e:
        return []
    finally:
        driver.quit()


# hackathons = devfolio_extractor()
# print(f"\nNo. of hackathons: {len(hackathons)}")
# for hackathon in hackathons:
#     print(f"\nName: {hackathon[0]}")
#     print(f"Link: {hackathon[1]}")
