from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

chrome_options = Options()
chrome_options.add_argument("--allow-insecure-localhost")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument(
    "--unsafely-treat-insecure-origin-as-secure=http://www.brightfutures.dcf.state.vt.us"
)
chrome_options.add_argument("--disable-blink-features=AutomationControlled")


# --- Configurable Constants ---
URL = "http://www.brightfutures.dcf.state.vt.us/vtcc/reset.do?0Mmr3gjumkz13-SgYEjWekr3%3dxguw3YEa.aU7zaju.xnn.xGOOF-Oq-Gq%2bSS%256UOq%256UhS.0DGgwEkeUs3peYY.wjRszYgwUVm3kmLmkkUs_umUkYAgsUWVjUVm3mWgwkmpwUVm31mLUjsegkz13SG0DqOqGqS0FO_SD"
DISTANCE = "30"  # miles
TOWN_VALUE = (
    "East Montpelier"  # dropdown <option value="..."> value attribute, not the label
)
OUTPUT_CSV = "links.csv"

# --- Selectors ---
DISTANCE_INPUT_ID = "field_distance3"
TOWN_DROPDOWN_ID = "field_town3"
SUBMIT_BUTTON_XPATH = "//input[@type='submit' and @value='Search']"
RESULT_LINKS_XPATH = "//table//a[normalize-space(text())='Details']"
NEXT_BUTTON_XPATH = "//a[text()='next>']"

# --- Start Browser ---
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 10)
driver.get(URL)

# --- Fill and Submit the Form ---
wait.until(EC.presence_of_element_located((By.ID, DISTANCE_INPUT_ID)))
driver.find_element(By.ID, DISTANCE_INPUT_ID).clear()
driver.find_element(By.ID, DISTANCE_INPUT_ID).send_keys(DISTANCE)

Select(driver.find_element(By.ID, TOWN_DROPDOWN_ID)).select_by_visible_text(TOWN_VALUE)

driver.find_element(By.XPATH, SUBMIT_BUTTON_XPATH).click()

# --- Collect Links ---
all_links = []

while True:
    wait.until(EC.presence_of_all_elements_located((By.XPATH, RESULT_LINKS_XPATH)))
    time.sleep(1)  # allow all content to settle
    links = driver.find_elements(By.XPATH, RESULT_LINKS_XPATH)
    new_links = [link.get_attribute("href") for link in links]
    all_links.extend(new_links)
    print(f"Collected {len(new_links)} links")

    # Check for next page
    try:
        next_button = driver.find_element(By.XPATH, NEXT_BUTTON_XPATH)
        next_button.click()
        time.sleep(1)
    except:
        print("No more pages.")
        break

# --- Write to CSV ---
with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    for link in all_links:
        writer.writerow([link])

print(f"\n✅ Saved {len(all_links)} links to {OUTPUT_CSV}")
driver.quit()
