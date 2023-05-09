from selenium import webdriver
import pandas as pd

# Define the URL of the match page
url = 'https://paladins.guru/match/1220879782'

# Set up the Selenium driver
driver = webdriver.Chrome() # Replace with the path to your Chrome driver executable
driver.get(url)

# Find the game mode and game queue sections and extract their values
game_mode = driver.find_element_by_css_selector('.card-header__match-info-text').text.strip()
game_queue = driver.find_element_by_css_selector('.card-header__match-info-queue').text.strip()

# Create a pandas DataFrame to store the extracted data
df = pd.DataFrame({
    'Game Mode': [game_mode],
    'Game Queue': [game_queue]
})

# Print the DataFrame
print(df)

# Close the Selenium driver
driver.quit()
