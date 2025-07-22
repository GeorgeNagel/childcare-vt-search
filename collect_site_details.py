import csv
import json
from pathlib import Path
import time
import re
from datetime import date

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# --- Input and Output ---
INPUT_CSV = "links.csv"
DATA_DIRECTORY = "data"
OUTPUT_CSV = "daycare_details.csv"

# --- Hardcoded XPaths (based on your input) ---
XPATH_NAME = "/html/body/table[3]/tbody/tr/td/form/table/tbody/tr[1]/td/table/tbody/tr/td[1]/span[2]"
XPATH_ADDRESS = "/html/body/table[3]/tbody/tr/td/form/table/tbody/tr[3]/td/table/tbody/tr[1]/td[5]/span"
XPATH_INFANT_VACANCY = (
    "/html/body/table[3]/tbody/tr/td/form/table/tbody/tr[6]/td/table/tbody/tr[2]/td[11]"
)
XPATH_TODDLER_VACANCY = (
    "/html/body/table[3]/tbody/tr/td/form/table/tbody/tr[6]/td/table/tbody/tr[3]/td[11]"
)

# --- Initialize driver ---
chrome_options = Options()
chrome_options.add_argument("--allow-insecure-localhost")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument(
    "--unsafely-treat-insecure-origin-as-secure=http://www.brightfutures.dcf.state.vt.us"
)
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(5)  # adjust if needed


def slugify(name):
    name = name.lower()
    name = re.sub(r"[^\w\s-]", "", name)
    name = re.sub(r"[\s_-]+", "-", name)
    return name.strip("-")


# --- Load URLs ---
data_path = Path(DATA_DIRECTORY)
with open(data_path / INPUT_CSV, newline="") as f:
    urls = [row[0] for row in csv.reader(f) if row]


# --- Helper function ---
def get_text_by_xpath(xpath, fallback="???"):
    try:
        return driver.find_element(By.XPATH, xpath).text.strip()
    except:
        return fallback


# --- Scrape and write each row immediately ---
for i, url in enumerate(urls, 1):
    driver.get(url)
    time.sleep(1)

    name = get_text_by_xpath(XPATH_NAME)
    address = get_text_by_xpath(XPATH_ADDRESS)
    infant = get_text_by_xpath(XPATH_INFANT_VACANCY)
    toddler = get_text_by_xpath(XPATH_TODDLER_VACANCY)

    # Check if an output file already exists for this provider
    filename = slugify(name) + ".json"
    output_path = data_path / filename
    metadata = {"name": name, "address": address, "slug": slugify(name)}

    if output_path.exists():
        with open(output_path, "r") as f:
            availability = json.load(f)["availability"]
    else:
        availability = {}

    todays_date = date.today().isoformat()
    current_availability = {
        "infant": infant,
        "toddler": toddler,
    }
    availability[todays_date] = current_availability

    with open(output_path, "w") as f:
        output_data = {"metadata": metadata, "availability": availability}
        json.dump(output_data, f, indent=2)

    print(f"[{i}/{len(urls)}] Scraped: {name}")

driver.quit()
print(f"\n✅ Done")
