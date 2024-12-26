#!/usr/bin/env python3
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from time import sleep
from bs4 import BeautifulSoup
import pandas as pd
import logging

# Set up Selenium options (optional, to run without a browser window)
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no UI)
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Path to your WebDriver (ChromeDriver in this case)
driver_path = "chromedriver-mac-arm64/chromedriver"

service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

def find_matches(user_profile):
    url = "https://paladins.guru" + user_profile + "/matches"
    try:
        driver.get(url)
        sleep(3) 
        print("found page")
        soup = BeautifulSoup(driver.page_source, "html.parser")

        section = soup.find(id="w")
        section = soup.find(id="cw", recursive=False)
        print("cw")
        # good to here
        section = section.find_next()
        section = section.find("section", recursive=False)
    
        section = section.find("div", class_="container", recursive=False)
        print("container")
        section = section.find("div", class_="columns", recursive=False)
        print("columns")
        section = section.find("div", class_="column col-8 col-md-12")
        print("column col-8")
        for match_div in section.find_all("div", recursive=False)[1:]:
             header = match_div.find(class_="top").find(class_="d-flex")
             print(header.find("a").get("href"))

        return None
    except Exception as e:
            logging.error(f"Error finding matches for user {user_profile}: {e}")
            return None


with open("profiles.txt", "r") as file:
    for line in file:
        line = line.strip()
        if line:
            match_id = line
            text = find_matches(match_id)
            if text:
                print(f"{match_id}\n{text}")