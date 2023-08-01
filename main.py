from functions_updating import create_json, read_json, add_to_json, update_dupes_json, establish_db_connection, insert_damage_breakdown_data_to_db, commit_and_close_db_connection, insert_match_data_to_db, insert_player_data_to_db
import pandas as pd

conn = establish_db_connection()
cursor = conn.cursor()


def win_percentage(champion):
    query = "SELECT * FROM `damage_breakdown` WHERE champion = '{}'".format(champion)
    cursor.execute(query)

    column_names = [desc[0] for desc in cursor.description]

    df = pd.DataFrame(cursor.fetchall(), columns=column_names)

    win_count = len(df[df['win_loss'] == 'W'])
    total_count = len(df)
    win_ratio = win_count / total_count
    print(round(win_ratio, 3))


def best_picks_given(champion):
    query = "SELECT match_id, win_loss,GROUP_CONCAT(champion) AS champions FROM paladins.damage_breakdown WHERE " \
            "match_id IN ( SELECT match_id FROM paladins.damage_breakdown WHERE champion IN ('Inara') GROUP BY " \
            "match_id HAVING COUNT(DISTINCT champion) = 1)	GROUP BY match_id, win_loss"
    cursor.execute(query)

    column_names = [desc[0] for desc in cursor.description]

    df = pd.DataFrame(cursor.fetchall(), columns=column_names)

    df['champions'] = df['champions'].str.split(',')

    teammates = {}
    opponents = {}
    for row_index, row in df.iterrows():
        if champion in row[-1]:
            for key in row[-1]:
                value = teammates.get(key, [0, 0])
                if 'W' in row:
                    value[0] += 1
                value[1] += 1
                teammates[key] = value
        else:
            for key in row[-1]:
                value = opponents.get(key, [0, 0])
                if 'W' in row:
                    value[0] += 1
                value[1] += 1
                opponents[key] = value



