#!/usr/bin/env python3
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from time import sleep
from bs4 import BeautifulSoup

# Set up Selenium options (optional, to run without a browser window)
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no UI)
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Path to your WebDriver (ChromeDriver in this case)
driver_path = "chromedriver-mac-arm64/chromedriver"

service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

def extract_data_from_html(url):
    """Extract text from a URL using Selenium to render the page."""
    try:
        driver.get(url)
        sleep(3) 

        soup = BeautifulSoup(driver.page_source, "html.parser")
        #damage insight
        parent_div = soup.find(id="insight-damage")

        return parent_div.get_text(strip=True)
    except Exception as e:
        return None

# The map function
for line in sys.stdin:
    line = line.strip()
    if line:
        url = line
        text = extract_data_from_html(url)
        if text:
            print(f"{url}\t{text}")

driver.quit()
