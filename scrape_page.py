# THIS ONE WORKS

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


def scrape_match(match_id):

    # create options object
    chrome_options = Options()

    # set headless option to true
    chrome_options.add_argument('--headless')

    # create webdriver instance
    driver = webdriver.Chrome(options=chrome_options)

    # match ID ex.
    # match_id = 1220879782

    # navigate to the page
    driver.get(f"https://paladins.guru/match/{match_id}")

    # get date
    try:
        span_tag = driver.find_element(By.CSS_SELECTOR, 'span[data-tooltip]')
        date = span_tag.get_attribute('data-tooltip')
    except NoSuchElementException:
        date = "N/A"

    # get game mode
    try:
        game_mode_text = driver.find_element(By.CSS_SELECTOR, 'h1[data-v-2e77aec3]')
        game_mode = game_mode_text.text.strip()
    except NoSuchElementException:
        game_mode = "N/A"

    # find the winners table
    try:
        # find all match-table win divs
        match_div = driver.find_element(By.CSS_SELECTOR, 'div.match-table.win')
        body_div = match_div.find_element(By.CSS_SELECTOR, 'div.match-table__body')
        row_divs = body_div.find_elements(By.CSS_SELECTOR, 'div.row.match-table__row')
        winners = []
        for div in row_divs:
            try:
                player_div = div.find_element(By.CSS_SELECTOR, 'div.row__player')
                div_element = player_div.find_element(By.CSS_SELECTOR, 'div[data-v-141fab60]')
                champion_name_div = div_element.find_element(By.CSS_SELECTOR, 'div[data-v-141fab60]')
                champion_name = champion_name_div.text
                winners.append(champion_name)
            except NoSuchElementException:
                pass
    except NoSuchElementException:
        winners = "N/A"

    # find the losers table
    try:
        # find all match-table loss divs
        match_div = driver.find_element(By.CSS_SELECTOR, 'div.match-table.loss')
        body_div = match_div.find_element(By.CSS_SELECTOR, 'div.match-table__body')
        row_divs = body_div.find_elements(By.CSS_SELECTOR, 'div.row.match-table__row')
        losers = []
        for div in row_divs:
            try:
                player_div = div.find_element(By.CSS_SELECTOR, 'div.row__player')
                div_element = player_div.find_element(By.CSS_SELECTOR, 'div[data-v-141fab60]')
                champion_name_div = div_element.find_element(By.CSS_SELECTOR, 'div[data-v-141fab60]')
                champion_name = champion_name_div.text
                losers.append(champion_name)
            except NoSuchElementException:
                pass
    except NoSuchElementException:
        losers = "N/A"
    # try:
    #     div_tags = driver.find_elements(By.CSS_SELECTOR, 'div[data-v-141fab60]')
    #     for div_tag in div_tags:
    #         print(div_tag.text)
    # except NoSuchElementException:
    #     div_tags = "N/A"

    # add to df
    new_row = {
        'Match ID': match_id,
        'Date': date,
        'Game Mode': game_mode,
        'Winners': winners,
        'Losers': losers
    }

    # close the webdriver instance
    driver.quit()
    return new_row
