from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import os


load_dotenv()

url = os.getenv("URL")
scraped_data_dir = os.getenv("SCRAPED_DATA_DIR")
log_file = os.getenv("LOG_FILE")

table_attribs = [
    "Contract",
    "Opening Price",
    "High",
    "Low",
    "Volume",
    "Turnover",
    "Open Interest",
    "Open Interest Change",
    "Closing Price",
    "Settlement Price",
    "Previous Settlement Price",
    "Price Change1",
    "Price Change2",
]

def log_progress(message):
    """Log progress messages with a timestamp."""
    timestamp_format = "%Y-%h-%d-%H:%M:%S"
    now = datetime.now()
    timestamp = now.strftime(timestamp_format)
    with open(log_file, "a") as f:
        f.write(timestamp + " : " + message + "\n")

def extract_with_selenium(url, table_attribs):
    """Extract data from the webpage using Selenium and save it as a DataFrame."""
    log_progress("Starting data extraction with Selenium.")

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
   # driver = webdriver.Chrome()

    try:
        driver.get(url)
        import time
        time.sleep(5)  
        page_source = driver.page_source
    except Exception as e:
        log_progress(f"Error during Selenium execution: {e}")
        raise
    finally:
        driver.quit()

    data = BeautifulSoup(page_source, "html.parser")
    df = pd.DataFrame(columns=table_attribs)

    table = data.find("div", class_="futures-table").find("table")
    tbody = table.find("tbody")
    if not tbody:
        log_progress("No <tbody> found on the page. Returning empty DataFrame.")
        return df

    rows = tbody.find_all("tr")
    log_progress(f"Total rows found: {len(rows)}")

    for row in rows:
        cols = row.find_all("td")
        if len(cols) < len(table_attribs):
            log_progress(f"Skipping incomplete row: {[col.text for col in cols]}")
            continue

        row_data = [col.text.strip().replace(",", "") for col in cols]
        data_dict = dict(zip(table_attribs, row_data))
        df = pd.concat([df, pd.DataFrame([data_dict])], ignore_index=True)

    log_progress("Data extraction completed.")
    return df

def save_to_scraped_data_dir(df, scraped_data_dir):
    """Save DataFrame as a CSV file in the scraped_data directory with a timestamp."""
    os.makedirs(scraped_data_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    csv_filename = f"{scraped_data_dir}/data_{timestamp}.csv"

    try:
        df.to_csv(csv_filename, index=False)
        log_progress(f"Data saved to {csv_filename}")
    except Exception as e:
        log_progress(f"Failed to save CSV: {e}")
        raise

if __name__ == "__main__":
    log_progress("Initiating extraction process.")
    df_extracted = extract_with_selenium(url, table_attribs)
    print("\nExtracted Data:\n")
    print(df_extracted)
    save_to_scraped_data_dir(df_extracted, scraped_data_dir)
