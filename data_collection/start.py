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

def extract_data_from_html(match_id):
    """Extract text from a URL using Selenium to render the page."""
    url = "https://paladins.guru/match/" + match_id
    try:
        driver.get(url)
        sleep(3) 

        soup = BeautifulSoup(driver.page_source, "html.parser")



        # map
        parent_div = soup.find(class_="page-header")
        map_div = parent_div.find(class_="page-header__div text-right")
        map = map_div.find("h2").get_text(strip=True)

        
        # match stats
        players = {}
        column_names = ["username", "champ_level", "k", "d", "a", "credits", "cpm"]
        parent_div = soup.find(id="match-stats")
        for team_div in parent_div.find_all(class_="scrollable"):
            table_data = team_div.find(class_="match-table__body")
            for child_div in table_data.find_all("div", recursive=False):
                i = 0
                row = {}
                champion = None
                for row_item in child_div.find_all("div", recursive=False)[:5]:
                    if i == 0:
                        data = row_item.find("div", recursive=False)
                        data = data.find_all(recursive=False)
                        row[column_names[i]] = data[0].get_text(strip=True)
                        link = data[0].get("href") 
                        print(link)
                        champion = data[1].get_text(strip=True)
                    elif i==2:
                        # k, d, a
                        row[column_names[i]], row[column_names[i+1]], row[column_names[i+2]] = row_item.get_text(strip=True).split(' / ')
                        i += 2
                    else:
                        row[column_names[i]] = row_item.get_text(strip=True)
                    i+=1
                players[champion] = row

        #damage insight

        column_names = ["win_loss", "champion", "damage", "weapon", "healing", "self_heal", "taken", "shielding"]

        parent_div = soup.find(id="insight-damage")
        table_data = parent_div.find(class_="columns", recursive=False)
        table_data = table_data.find(class_="match-table__body")
        for child_div in table_data.find_all("div", recursive=False):
            row = {}
            for column_name, row_item in zip(column_names, child_div.find_all("div", recursive=False)[:8]):
                if column_name != "champion":
                    row[column_name] = row_item.get_text(strip=True)
                else:
                    data = row_item.find("div", recursive=False)
                    row["champion"] = data.find("div", recursive=False).get_text(strip=True)

            players[row["champion"]].update(row)

        df = pd.DataFrame([
            {**stats, "map": map, "match_id": match_id} 
            for stats in players.values()
        ])

        return df
    except Exception as e:
        logging.error(f"Error processing match ID {match_id}: {e}")
        return None

# The map function
with open("match_ids.txt", "r") as file:
    for line in file:
        line = line.strip()
        if line:
            match_id = line
            text = extract_data_from_html(match_id)
            if not text.empty:
                print(f"{match_id}\n{text}")

driver.quit()
