import mysql.connector
import json
import os
from dotenv import load_dotenv

load_dotenv()
DATABSE_PASSWORD = os.getenv("DATABSE_PASSWORD")
DATABSE_DATABASE = os.getenv("DATABSE_DATABASE")

# Define the database connection function
def establish_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password=DATABSE_PASSWORD,
        database=DATABSE_DATABASE
    )
    print("successfully connected to database")
    return conn


def insert_match_data_to_db(cursor, data):
    insert_query = "INSERT INTO `match` (match_id, date, match_length, game_mode, team_one_score, team_two_score, " \
                   "winning_team, map, ban_1, ban_2, ban_3, ban_4 ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
                   "%s, %s)"
    cursor.execute(insert_query, data)
    print("succesfully added match data")


def insert_player_data_to_db(cursor, data):
    insert_query = "INSERT INTO `player` (match_id, team_number, champion, username, pick_number, level, kills, " \
                   "deaths, assists, credits) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(insert_query, data)
    print("succesfully added player data")


def insert_damage_breakdown_data_to_db(cursor, data):
    insert_query = "INSERT INTO `damage_breakdown` (match_id, win_loss, username, champion, damage_total, " \
                   "damage_weapon, healing, self_heal, damage_taken, shielding) VALUES (%s, %s, %s, %s, %s, %s, " \
                   "%s, %s, %s, %s)"
    cursor.execute(insert_query, data)
    print("succesfully added damage breakdown")


def commit_and_close_db_connection(conn, cursor):
    cursor.close()
    conn.close()
    print("succesfully closed database")


def create_json(file_name):
    file_path = r'C:\Users\SummerlyCow\Desktop\Paladins-Ranker\data\{}.json'.format(file_name)

    # write empty json file
    open(file_path, 'w')
    print("json created")


def read_json(file_name):
    file_path = r'C:\Users\SummerlyCow\Desktop\Paladins-Ranker\data\{}.json'.format(file_name)

    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        # Read existing data from JSON file
        with open(file_path, "r") as file:
            data_list = json.load(file)
            data_set = set(data_list)
    else:
        # Initialize an empty list if the file is empty
        data_set = set()
    return data_set


def add_to_json(file_name, new_data, cursor):
    file_path = r'C:\Users\SummerlyCow\Desktop\Paladins-Ranker\data\{}.json'.format(file_name)

    data_set = read_json(file_path)

    # Append new data to the existing list
    for i in new_data:
        data_set.add(i)

    # gets all match ids already in database
    file_path = r'C:\Users\SummerlyCow\Desktop\Paladins-Ranker\data\{}.json'.format(file_name)
    query = "SELECT match_id FROM `match`"
    cursor.execute(query)
    db_match_ids = cursor.fetchall()

    # O(n), iterate through database match ids and use discard() to remove from data_set, so only removes dupes and ignores otherwise
    for i in db_match_ids:
        data_set.discard(i)

    # Write the updated data back to the JSON file
    with open(file_path, "w") as file:
        json.dump(data_set, file)

    print("Data added to JSON file.")
    print(str(len(data_set)) + " match ids in file")
