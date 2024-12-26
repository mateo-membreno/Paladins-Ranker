from web_scraping.functions_scraping import find_match_ids_by_player, scrape_page
from web_scraping.functions_update_db import create_json, read_json, add_to_json, establish_db_connection, insert_damage_breakdown_data_to_db, commit_and_close_db_connection, insert_match_data_to_db, insert_player_data_to_db

# establish connection and cursor
conn = establish_db_connection()
cursor = conn.cursor()

# read in match ids from json file as set
match_ids = read_json("match_ids")
print(len(match_ids), match_ids)

# initialize counter for pages scraped
count = 0
for ID in match_ids:
    # if this doesn't work match ID is expired
    try:
        data = scrape_page(ID)
        count += 1
        print(count)
    except:
        print("\033[91mPage not available for {}\033[0m".format(ID))

    # if this doesn't work then deleted accounts were being used
    try:
        insert_match_data_to_db(cursor, data[0])

        for i in data[1]:
            insert_player_data_to_db(cursor, i)
        for i in data[2]:
            insert_damage_breakdown_data_to_db(cursor, i)
        conn.commit()
    except:
        print("\033[91mMissing data for {}\033[0m".format(ID))
        continue


commit_and_close_db_connection(conn, cursor)
