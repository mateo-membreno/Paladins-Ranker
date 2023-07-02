import mysql.connector
import json
import os


# Define the database connection function
def establish_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="maxmembreno$",
        database="paladins"
    )
    print("successfully connected to database")
    return conn


def insert_match_data_to_db(cursor, data):
    insert_query = "INSERT INTO `match` (match_id, date, match_length, game_mode, team_one_score, team_two_score, " \
                   "winning_team, map) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
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


def add_to_json(file_name, new_data):
    file_path = r'C:\Users\SummerlyCow\Desktop\Paladins-Ranker\data\{}.json'.format(file_name)

    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        # Read existing data from JSON file
        with open(file_path, "r") as file:
            data_list = json.load(file)
    else:
        # Initialize an empty list if the file is empty
        data_list = []

    # Append new data to the existing list
    for i in new_data:
        data_list.append(i)

    # remove duplicates
    unique_data_list = []
    for item in data_list:
        if item not in unique_data_list:
            unique_data_list.append(item)

    # Write the updated data back to the JSON file
    with open(file_path, "w") as file:
        json.dump(unique_data_list, file)

    print("Data added to JSON file.")
    print(str(len(unique_data_list)) + " match ids in file")


def read_json(file_name):
    file_path = r'C:\Users\SummerlyCow\Desktop\Paladins-Ranker\data\{}.json'.format(file_name)

    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        # Read existing data from JSON file
        with open(file_path, "r") as file:
            data_list = json.load(file)
    else:
        # Initialize an empty list if the file is empty
        data_list = []
    return data_list

def remove_from_json(file_name)
