import sqlite3
import pandas as pd

def store_match_data(df):
    try:
        df['champ_level'] = df['champ_level'].astype(int)
        df['k'] = df['k'].astype(int)
        df['d'] = df['a'].astype(int)
        df['a'] = df['a'].astype(int)
        df['credits'] = df['credits'].replace({',': ''}, regex=True).astype(int)
        df['cpm'] = df['cpm'].astype(int)
        df['damage'] = df['damage'].replace({',': ''}, regex=True).astype(int)
        df['weapon'] = df['weapon'].replace({',': ''}, regex=True).astype(int)
        df['healing'] = df['healing'].replace({',': ''}, regex=True).astype(int)
        df['self_heal'] = df['self_heal'].replace({',': ''}, regex=True).astype(int)
        df['taken'] = df['taken'].replace({',': ''}, regex=True).astype(int)
        df['shielding'] = df['shielding'].replace({',': ''}, regex=True).astype(int)

        conn = sqlite3.connect("../paladins.db")
        df.to_sql("match", conn, if_exists="append", index=False)
        conn.close()
    except Exception as e:
                print(f"Error storing match data in db: {e}")