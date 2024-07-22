import sqlite3 as sq
import mysql.connector
import os
import pandas as pd
import csv
from dotenv import load_dotenv

load_dotenv()

DATABSE_PASSWORD = os.getenv('DATABASE_PASSWORD')

mysql_conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password=DATABSE_PASSWORD,
        database="paladins"
    )
mysql_cursor = mysql_conn.cursor()

# Export data from MySQL to CSV
tables = ['player', '`match`', 'damage_breakdown']
csv_files = ['player.csv', 'match.csv', 'damage_breakdown.csv']

for table, csv_file in zip(tables, csv_files):
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        mysql_cursor.execute(f"SELECT * FROM {table}")
        rows = mysql_cursor.fetchall()
        writer.writerows(rows)
        print("wrote {table}")

mysql_conn.close()
mysql_conn.close()