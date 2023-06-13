import pyspark as sc
from pyspark.sql import SparkSession
import pandas as pd
import requests
from bs4 import BeautifulSoup
from scrape_page import scrape_match

spark = SparkSession.builder.getOrCreate()

base_url = 'https://paladins.guru/match/'
match_ids = range(1220879781, 1220879799)


# create df columns
df = pd.DataFrame(columns=['Match ID', 'Date', 'Game Mode', 'Winners', 'Losers'])

# iterate over all match numbers
for match_id in range(1220879781, 1220879783):
    url = f'{base_url}{match_id}'
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the response is successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Perform further scraping operations as needed
        new_row = scrape_match(match_id)
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        print(f"Match {match_id} scraped")


    else:
        # Handle unsuccessful responses or missing pages
        print(f"Match {match_id} not found or inaccessible")

print(df)
