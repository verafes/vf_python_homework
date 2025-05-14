from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

# Task
url = "https://owasp.org/www-project-top-ten/"

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(service=ChromeService(), options=chrome_options)
    return driver

driver = get_driver()

try:
    driver.get(url)

    wait = WebDriverWait(driver, 10)

    # Wait until the main content loads (till section after the top-10 list)
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".member-list")))

    items_locator = "//h2[@id='top-10-web-application-security-risks']/../ul/li/a"
    items = wait.until(EC.presence_of_all_elements_located((By.XPATH, items_locator)))

    top_10_links = []

    for item in items:
        title = item.text.strip()
        link = item.get_attribute("href")
        top_10_links.append({
            "Title": title,
            "Link": link
        })

    for entry in top_10_links:
        print(entry)

except Exception as e:
    print(f"An exception occurred: {type(e).__name__} {e}")
finally:
    driver.quit()

# Save to CSV
try:
    csv_file = "owasp_top_10.csv"
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["Title", "Link"])
        writer.writeheader()
        writer.writerows(top_10_links)
    print("Data successfully saved")
except IOError as e:
    print(f"Failed to write to CSV: {e}")
except Exception as ex:
    print(f"An unexpected error occurred: {ex}")