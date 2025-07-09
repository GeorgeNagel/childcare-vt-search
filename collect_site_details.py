import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# --- Input and Output ---
INPUT_CSV = "links.csv"
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
chrome_options.add_argument(
    "--unsafely-treat-insecure-origin-as-secure=http://www.brightfutures.dcf.state.vt.us"
)
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(5)  # adjust if needed

# --- Load URLs ---
with open(INPUT_CSV, newline="") as f:
    urls = [row[0] for row in csv.reader(f) if row]


# --- Load URLs ---
with open(INPUT_CSV, newline="") as f:
    urls = [row[0] for row in csv.reader(f) if row]

# --- Open CSV and write header first ---
with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, quoting=csv.QUOTE_ALL)
    writer.writerow(
        ["Name", "Address", "Infant Vacancies", "Toddler Vacancies", "Source URL"]
    )

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

        row = [name, address, infant, toddler, url]
        writer.writerow(row)
        f.flush()  # ensure it's written to disk immediately

        print(f"[{i}/{len(urls)}] Scraped: {name}")

driver.quit()
print(f"\n✅ Done: saved all records to '{OUTPUT_CSV}'")
