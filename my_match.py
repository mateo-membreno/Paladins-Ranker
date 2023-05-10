#THIS ONE WORKS
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# create df columns
df = pd.DataFrame(columns=['Match ID', 'Date', 'Game Mode'])

# create options object
chrome_options = Options()

# set headless option to true
chrome_options.add_argument('--headless')

# create webdriver instance
driver = webdriver.Chrome(options=chrome_options)

# match ID
match_ID = 1220879782

# navigate to the page
driver.get(f"https://paladins.guru/match/{match_ID}")

# get game mode
try:
    game_mode_text = driver.find_element(By.CSS_SELECTOR, 'h1[data-v-2e77aec3]')
    game_mode = game_mode_text.text.strip()
except NoSuchElementException:
    game_mode = "N/A"

# get players
try:
    span_tag = driver.find_element(By.CSS_SELECTOR, 'span[data-tooltip]')
    date = span_tag.get_attribute('data-tooltip')
except NoSuchElementException:
    date = "N/A"


# create a dictionary with the game mode text
data = {'Game Mode': [game_mode]}

# create a dataframe from the dictionary
df = pd.DataFrame(data)
print(df)

# close the webdriver instance
driver.quit()
