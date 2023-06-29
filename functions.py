import mysql.connector
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


# Define the database connection function
def establish_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password=input("password?"),
        database="your_database"
    )
    return conn


# Define the web scraping function
def scrape_page(match_url):
    # Perform web scraping logic here
    # create options object
    chrome_options = Options()

    # set headless option to true
    chrome_options.add_argument('--headless')

    # create webdriver instance
    driver = webdriver.Chrome(options=chrome_options)

    # match ID .
    match_id = int(match_url.split("/match/")[1])

    # navigate to the page
    driver.get(f"{match_url}")

    # get date
    try:
        span_tag = driver.find_element(By.CSS_SELECTOR, 'span[data-tooltip]')
        date = span_tag.get_attribute('data-tooltip')
        datetime_obj = datetime.strptime(date, '%A, %B %d, %Y %I:%M %p')
        date = datetime_obj.strftime('%Y-%m-%d %H:%M:%S')
    except NoSuchElementException:
        date = "N/A"

    # get game mode
    # get match length
    try:
        game_mode_text = driver.find_element(By.CSS_SELECTOR, 'h1[data-v-2e77aec3]')
        match_length_text = driver.find_element(By.CSS_SELECTOR, 'h3[data-v-2e77aec3]')
        game_mode = game_mode_text.text.strip()
        match_length = int(match_length_text.text.strip().split()[3])
    except NoSuchElementException:
        game_mode = "N/A"
        match_length = "N/A"

    # get map
    map_class = driver.find_element(By.CSS_SELECTOR, 'h2[style="font-size: 1.6em; margin-bottom: 0; color: #f3f3f3"]')
    match_map = map_class.text.strip()

    # get score and winning team
    try:
        element = driver.find_element(By.CSS_SELECTOR, '#match-stats')
        team_divs = element.find_element(By.CSS_SELECTOR, 'div.columns')
        team_divs = team_divs.find_elements(By.CSS_SELECTOR, 'div.column')
        for i, team_div in enumerate(team_divs):
            print(i)
            if i == 0:
                score_div = team_div.find_element(By.CSS_SELECTOR, 'h1[data-v-09d5041f]')
                team_1_score = int(score_div.text)
                print(team_1_score)
            elif i == 2:
                score_div = team_div.find_element(By.CSS_SELECTOR, 'h1[data-v-09d5041f]')
                team_2_score = int(score_div.text)
        if team_2_score > team_1_score:
            winning_team_number = 2
        else:
            winning_team_number = 1
    except NoSuchElementException:
        team_2_score = -1
        team_1_score = -1
        winning_team_number = -1

    # add match info to list
    match = [match_id, date, match_length, game_mode, team_1_score, team_2_score, winning_team_number, match_map]

    # find the player info
    players = []
    try:
        # find all player divs
        element = driver.find_element(By.CSS_SELECTOR, '#match-stats')
        team_divs = element.find_elements(By.CSS_SELECTOR, 'div.scrollable')

        for team_number, team_div in enumerate(team_divs):
            body_div = team_div.find_element(By.CSS_SELECTOR, 'div.match-table__body')
            row_divs = body_div.find_elements(By.CSS_SELECTOR, 'div.row.match-table__row')
            for pick_number, div in enumerate(row_divs):
                player_div = div.find_element(By.CSS_SELECTOR, 'div.row__player')
                div_element = player_div.find_element(By.CSS_SELECTOR, 'div[data-v-141fab60]')
                div_user = player_div.find_element(By.CSS_SELECTOR, 'a.row__player__name')
                username = div_user.text
                champion_name_div = div_element.find_element(By.CSS_SELECTOR, 'div[data-v-141fab60]')
                champion_name = champion_name_div.text
                player_data = [match_id, team_number + 1, champion_name, username, pick_number + 1]
                div_row_items = div.find_elements(By.CSS_SELECTOR, 'div.row__item')
                for i, item_div in enumerate(div_row_items):
                    if i == 1:
                        content = item_div.get_attribute("innerHTML").split()
                        player_data.append(int(content[0]))
                        player_data.append(int(content[2]))
                        player_data.append(int(content[4]))
                    elif i == 0 or i == 2:
                        content = item_div.get_attribute("innerHTML")
                        player_data.append(int(content.replace(',', '')))
                    else:
                        break
                players.append(player_data)

    except NoSuchElementException:
        winners = "N/A"

    # find damage breakdown
    damage_breakdown = []
    section_element = driver.find_element(By.ID, "#match-insights")
    damage_div = section_element.find_element(By.ID, 'insight-damage')
    table_div = damage_div.find_element(By.CSS_SELECTOR, 'div.match-table__body')
    row_divs = table_div.find_elements(By.CSS_SELECTOR, 'div.row.match-table__row')
    for row in row_divs:
        individual = [match_id]
        row_data = row.text.split()
        for data in row_data:
            try:
                data = int(data.replace(',', ''))
                individual.append(data)
            except:
                individual.append(data)
        damage_breakdown.append(individual)
    driver.quit()
    return [match, players, damage_breakdown]


# Define the function to insert data into the database
def insert_match_data_to_db(conn, data):
    cursor = conn.cursor()
    # Execute SQL statements to insert data into the database
    insert_query = "INSERT INTO your_table (match_id, date, duration, game_mode, team_1_score, team_2_score, " \
                   "winning_team) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(insert_query, data)
    conn.commit()
    cursor.close()


def insert_player_data_to_db(conn, data):
    cursor = conn.cursor()
    # Execute SQL statements to insert data into the database
    insert_query = "INSERT INTO your_table (match_id, team_number, champion, player_number) VALUES (%s, %s, %s, %s, " \
                   "%s, %s, %s)"
    conn.commit()
    cursor.close()


def insert_damage_breakdown_data_to_db(conn, data):
    cursor = conn.cursor()
    # Execute SQL statements to insert data into the database
    insert_query = "INSERT INTO your_table (match_id, team_number, champion, player_number) VALUES (%s, %s, %s, %s, " \
                   "%s, %s, %s)"
    conn.commit()
    cursor.close()
