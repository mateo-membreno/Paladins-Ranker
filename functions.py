import mysql.connector


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
def scrape_page(page_url):
    # Perform web scraping logic here
    # ...
    scraped_data = ...
    return scraped_data


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
