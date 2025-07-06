from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

BRAVE_PATH = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"

options = Options()
options.binary_location = BRAVE_PATH
options.headless = True  # Set to True if you want headless

service = Service(executable_path="./chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

# Ask the user for input
user_input = input("Enter the show title or full link: ").strip()

if user_input.startswith("http"):
    driver.get(user_input)
else:
    driver.get("https://kisskh.do")
    time.sleep(5)

    try:
        # Click the search icon to reveal the search input
        search_icon = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.TAG_NAME, "app-search-bar"))
        )
        search_icon.click()
        time.sleep(3)
        print("Search icon clicked successfully.")

        # Wait for the search input to appear
        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "search"))
        )

        search_input.send_keys(user_input)
        time.sleep(5)  # Allow time for results to load
        # Wait for result dropdown
        results_list = driver.find_elements(By.TAG_NAME, "app-main-card")
        search_query = user_input.strip().lower()
        # Iterate and find exact match
        matched = False

        for item in results_list:
            title_element = item.find_element(By.TAG_NAME, "mat-card-title")
            title_text = title_element.text.strip().lower()
            print(f"Checking title: {title_text}")

            if title_text == search_query:
                print(f"Found exact match: {title_text}")
                title_element.click()
                matched = True
                break

        if not matched:
            print("❌ No exact match found.")
            driver.quit()
            exit()

    except Exception as e:
        print("Search failed:", e)
        driver.quit()
        exit()

# Let page load
time.sleep(3)

# Print current page title and URL for confirmation
print("Current Page:", driver.title)
print("URL:", driver.current_url)

# We'll pause here before scraping episodes
input("Press Enter to continue...")

driver.quit()
