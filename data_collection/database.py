import sqlite3

def store_match_data(df):

    df['champ_level'] = df['champ_level'].astype(int)
    df['k'] = df['k'].astype(int)
    df['d'] = df['a'].astype(int)
    df['a'] = df['a'].astype(int)
    df['credits'] = df['credits'].replace({',': ''}, regex=True).astype(int)
    df['cpm'] = df['cpm'].astype(int)
    df['damage'] = df['damage'].replace({',': ''}, regex=True).astype(int)
    df['weapon'] = df['weapon'].replace({',': ''}, regex=True).astype(int)
    df['healing'] = df['healing'].astype(int)
    df['self_heal'] = df['self_heal'].astype(int)
    df['taken'] = df['taken'].astype(int)
    df['shielding'] = df['shielding'].astype(int)

    conn = sqlite3.connect("paladins")
    df.to_sql("match", conn, if_exists="append", index=False)
    print(f"Data successfully stored in paladins.")
    conn.close()