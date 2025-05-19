from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

import pandas as pd
import json
from pprint import pprint


def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--sandbox")
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=ChromeService(), options=chrome_options)
    # driver.set_window_size(1900, 1000)
    return driver

# Task 1.  Review robots.txt
robots_url = "https://durhamcountylibrary.org/robots.txt"
def get_library_policy(driver):
    driver.get(robots_url)
    content = driver.page_source
    print(content)
    with open("robot.txt", "w") as file:
        file.write(content)

driver = get_driver()
get_library_policy(driver)

# Task 3: Write a Program to Extract this Data
book_url = "https://durhamcounty.bibliocommons.com/v2/search?query=learning%20spanish&searchType=smart"
def extract_books(driver):
    driver.get(book_url)

    li_locator = "li.cp-search-result-item"
    results = []
    max_pages = 10

    current_page = 1
    while current_page <= max_pages:
        print(f"Scraping page {current_page}")

        li_elements = WebDriverWait(driver, 10).until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, li_locator))
        )
        print(f"Found {len(li_elements)} items on page {current_page}")

        for item in li_elements:
            title = item.find_element(By.CSS_SELECTOR, "span.cp-screen-reader-message").text if item else "N/A"
            title = title.split(",")[0].strip()
            # print("title:", title)

            authors_elements = item.find_elements(By.CLASS_NAME, "author-link") if item else "N/A"
            author_texts = [author.text for author in authors_elements]
            author = "; ".join(author_texts)
            # print("author:", author)

            format_year = item.find_element(By.CSS_SELECTOR, "span.display-info-primary").text if item else "N/A"
            format_year = format_year.split("|")[0].strip()
            # print("format year:", format_year)

            results.append({
                "Title": title,
                "Author": author,
                "Format-Year": format_year
            })

        # Check if there is a "Next" page
        if current_page >= max_pages:
            print(f"Reached max page limit ({max_pages}).")
            break
        next_page = current_page + 1
        buttons = driver.find_elements(
            By.XPATH,
            f"//nav/ul[@class='pagination__desktop-items']/li[@class='cp-pagination-item pagination__page-number']/a[contains(@href,'page={next_page}')]"
        )
        if buttons:
            print(f"Moving to next page {next_page}...")
            next_page_href = buttons[0].get_attribute("href")
            driver.get(next_page_href)
            current_page += 1

        else:
            print("No more pages.")
            break

    print(len(results))
    pprint(results, sort_dicts=False)

    # Data Frame
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", None)
    pd.set_option("display.max_colwidth", None)

    df_results = pd.DataFrame(results)
    print(df_results)

    # Task 4. Save data to a CVS file
    df_results.to_csv("get_books.csv", index=False)

    # Save data to a JSON file
    with open("get_books.json", "w") as json_file:
        json.dump(results, json_file, indent=4)

extract_books(driver)
driver.quit()
