from functions_scraping import find_match_ids_by_player, scrape_page
from functions_updating import create_json, read_json, add_to_json, establish_db_connection, insert_damage_breakdown_data_to_db, commit_and_close_db_connection, insert_match_data_to_db, insert_player_data_to_db


conn = establish_db_connection()
cursor = conn.cursor()

match_ids = read_json("unscraped_match_ids")

for ID in match_ids:
    data = scrape_page(ID)

    insert_match_data_to_db(cursor, data[0])

    for i in data[1]:
        insert_player_data_to_db(cursor, i)
    for i in data[2]:
        insert_damage_breakdown_data_to_db(cursor, i)
    conn.commit()

commit_and_close_db_connection(conn, cursor)

