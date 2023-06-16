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



    # find the player info
    try:
        # find all player divs
        element = driver.find_element(By.CSS_SELECTOR, '#match-stats')
        team_divs = element.find_elements(By.CSS_SELECTOR, 'div.scrollable')
        players = []
        for team_number, team_div in enumerate(team_divs):
            body_div = team_div.find_element(By.CSS_SELECTOR, 'div.match-table__body')
            row_divs = body_div.find_elements(By.CSS_SELECTOR, 'div.row.match-table__row')
            for player_number, div in enumerate(row_divs):
                player_div = div.find_element(By.CSS_SELECTOR, 'div.row__player')
                div_element = player_div.find_element(By.CSS_SELECTOR, 'div[data-v-141fab60]')
                champion_name_div = div_element.find_element(By.CSS_SELECTOR, 'div[data-v-141fab60]')
                champion_name = champion_name_div.text
                player_data = [match_id, team_number+1, champion_name, player_number+1]
                players.append(player_data)
                # append player_data to database
                # Execute the INSERT statement
                cursor.execute(insert_query_player, data)
        print(players)
    except NoSuchElementException:
        winners = "N/A"





    # find the losers table
    # try:
    #     # find all match-table loss divs
    #     match_div = driver.find_element(By.CSS_SELECTOR, 'div.match-table.loss')
    #     body_div = match_div.find_element(By.CSS_SELECTOR, 'div.match-table__body')
    #     row_divs = body_div.find_elements(By.CSS_SELECTOR, 'div.row.match-table__row')
    #     losers = []
    #     for div in row_divs:
    #         try:
    #             player_div = div.find_element(By.CSS_SELECTOR, 'div.row__player')
    #             div_element = player_div.find_element(By.CSS_SELECTOR, 'div[data-v-141fab60]')
    #             champion_name_div = div_element.find_element(By.CSS_SELECTOR, 'div[data-v-141fab60]')
    #             champion_name = champion_name_div.text
    #             losers.append(champion_name)
    #         except NoSuchElementException:
    #             pass
    # except NoSuchElementException:
    #     losers = "N/A"

    # close the webdriver instance
    driver.quit()
    return 0


scrape_match(1222430362)
