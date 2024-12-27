#!/usr/bin/env python3
from bs4 import BeautifulSoup
import pandas as pd
import logging
import requests
import csv

def scrape_match_data(match_id):
    """Extract text from a URL using Selenium to render the page."""
    url = "https://paladins.guru/match/" + match_id
    try:
        response = requests.get(url)

        soup = BeautifulSoup(response.text, "html.parser")

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
        column_names = ["result", "champion", "damage", "weapon", "healing", "self_heal", "taken", "shielding"]

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
        logging.error(f"Error scraping page data at {match_id}: {e}")
        return None
    
        


def get_user_match_ids(user_profile):
    """Gets match ids from the first page of a player's match history."""
    url = f"https://paladins.guru/profile/{user_profile}/matches"
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        match_ids = [a['href'].split('/match/', 1)[1] for a in soup.find_all('a', href=True) if a['href'].startswith('/match/')]

        return match_ids
    except Exception as e:
            logging.error(f"Error finding matches for user {user_profile}: {e}")
            return None


def get_player_profiles(match_id):
    """Gets player profile link addresses from a match stats page."""
    url = f"https://paladins.guru/match/{match_id}"
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        profiles = [a['href'].split('/profile/', 1)[1] for a in soup.find_all('a', href=True) if a['href'].startswith('/profile/')]
        
        seen_profiles = set()
        filtered = []

        for profile in profiles:
            if profile not in seen_profiles:
                filtered.append(profile)
                seen_profiles.add(profile)

        return filtered
    except Exception as e:
        logging.error(f"Error finding profiles for {match_id}: {e}")
        return None
