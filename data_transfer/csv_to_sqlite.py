import sqlite3 as sq
import os
import pandas as pd
import csv

conn = sq.connect('paladins.db')
cursor = conn.cursor()

# Create tables in SQLite
create_match_table = """
CREATE TABLE IF NOT EXISTS match (
    match_id INTEGER PRIMARY KEY NOT NULL,
    date DATE NOT NULL,
    match_length INTEGER NOT NULL,
    game_mode VARCHAR(30) NOT NULL,
    team_one_score INTEGER NOT NULL,
    team_two_score INTEGER NOT NULL,
    winning_team INTEGER NOT NULL,
    map VARCHAR(30) NOT NULL,
    ban_1 VARCHAR(30) NOT NULL,
    ban_2 VARCHAR(30) NOT NULL,
    ban_3 VARCHAR(30) NOT NULL,
    ban_4 VARCHAR(30) NOT NULL
);
"""

create_player_table = """
CREATE TABLE IF NOT EXISTS player (
    match_id INTEGER NOT NULL,
    champion VARCHAR(30) NOT NULL,
    team_number INTEGER NOT NULL,
    username VARCHAR(30) NOT NULL,
    pick_number INTEGER NOT NULL,
    champ_level INTEGER NOT NULL,
    kills INTEGER NOT NULL,
    deaths INTEGER NOT NULL,
    assists INTEGER NOT NULL,
    credits INTEGER NOT NULL,
    PRIMARY KEY (match_id, champion)
);
"""

create_damage_breakdown_table = """
CREATE TABLE IF NOT EXISTS damage_breakdown (
    match_id INTEGER NOT NULL,
    champion VARCHAR(30) NOT NULL,
    username VARCHAR(30) NOT NULL,
    win_loss VARCHAR(30) NOT NULL,
    total_damage INTEGER NOT NULL,
    weapon_damage INTEGER NOT NULL,
    healing INTEGER NOT NULL,
    self_heal INTEGER NOT NULL,
    damage_taken INTEGER NOT NULL,
    shielding INTEGER NOT NULL,
    PRIMARY KEY (match_id, champion)
);
"""

# Execute table creation queries individually
with conn:
    conn.execute(create_match_table)
    conn.execute(create_player_table)
    conn.execute(create_damage_breakdown_table)

# Insert data into SQLite
# Query data from MySQL

def insert_data_from_csv(csv_file, table_name):
    count = 0
    df = pd.read_csv(csv_file)
    print(df.info())
    for index, row in df.iterrows():
        columns = ', '.join(df.columns)
        placeholders = ', '.join('?' * len(row))
        sql = f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders})'
        try:
            cursor.execute(sql, tuple(row))
        except sq.IntegrityError:
            count+=1
    print(count)

insert_data_from_csv('player.csv', 'player')
insert_data_from_csv('match.csv', 'match')
insert_data_from_csv('damage_breakdown.csv', 'damage_breakdown')



# merge player and damage breakdown table to reduce redunancy
create_player_data_table = """
CREATE TABLE IF NOT EXISTS player_data (
    match_id INTEGER NOT NULL,
    champion VARCHAR(30) NOT NULL,
    team_number INTEGER NOT NULL,
    username VARCHAR(30) NOT NULL,
    pick_number INTEGER NOT NULL,
    champ_level INTEGER NOT NULL,
    kills INTEGER NOT NULL,
    deaths INTEGER NOT NULL,
    assists INTEGER NOT NULL,
    credits INTEGER NOT NULL,
    win_loss VARCHAR(30) NOT NULL,
    total_damage INTEGER NOT NULL,
    weapon_damage INTEGER NOT NULL,
    healing INTEGER NOT NULL,
    self_heal INTEGER NOT NULL,
    damage_taken INTEGER NOT NULL,
    shielding INTEGER NOT NULL,
    PRIMARY KEY (match_id, champion)
);
"""

cursor.execute(create_player_data_table)

insert_player_data = """
INSERT INTO player_data (
    match_id, champion, team_number, username, pick_number, champ_level, kills, deaths, assists, credits,
    win_loss, total_damage, weapon_damage, healing, self_heal, damage_taken, shielding
)
SELECT
    p.match_id,
    p.champion,
    p.team_number,
    p.username,
    p.pick_number,
    p.champ_level,
    p.kills,
    p.deaths,
    p.assists,
    p.credits,
    d.win_loss,
    d.total_damage,
    d.weapon_damage,
    d.healing,
    d.self_heal,
    d.damage_taken,
    d.shielding
FROM
    player p
JOIN
    damage_breakdown d
ON
    p.match_id = d.match_id
    AND p.champion = d.champion;
"""

cursor.execute(insert_player_data)

df = pd.read_sql_query('select * from player_data', conn)
print(df.info())
conn.commit()
conn.close()