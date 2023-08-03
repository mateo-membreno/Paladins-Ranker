import pandas as pd


def win_percentage(champion, cursor):
    """
    Calculate the win percentage of a given champion in the 'damage_breakdown' table.

    Parameters:
        champion (str): The name of the champion for which the win percentage is calculated.
        cursor: A MySQL cursor object to execute the database query.

    Returns:
        None

    Prints:
        The win percentage of the champion rounded to three decimal places.

    Raises:
        None

    Example Usage:
        # Assuming 'cursor' is a MySQL cursor object
        win_percentage('Fernando', cursor)
    """

    # Form the SQL query to select data for the given champion
    query = "SELECT * FROM `damage_breakdown` WHERE champion = '{}'".format(champion)
    cursor.execute(query)

    # Get column names from the query result
    column_names = [desc[0] for desc in cursor.description]

    # Create a DataFrame from the query result
    df = pd.DataFrame(cursor.fetchall(), columns=column_names)

    # Calculate the number of wins and total matches played for the champion
    win_count = len(df[df['win_loss'] == 'W'])
    total_count = len(df)

    # Calculate the win ratio and print it rounded to three decimal places
    win_ratio = win_count / total_count
    print(round(win_ratio, 3))


def best_picks_given(target_champions, cursor):
    query = """
        SELECT match_id, win_loss, GROUP_CONCAT(champion) AS champions
        FROM paladins.damage_breakdown
        WHERE match_id IN (
            SELECT match_id
            FROM paladins.damage_breakdown
            WHERE champion in ({0}) and win_loss = 'W'
            GROUP BY match_id
            HAVING COUNT(DISTINCT champion) = {1}
        ) or match_id IN(
            SELECT match_id
            FROM paladins.damage_breakdown
            WHERE champion in ({0}) and win_loss = 'L'
            GROUP BY match_id
            HAVING COUNT(DISTINCT champion) = {1}
        )
        GROUP BY match_id, win_loss
        """.format(', '.join(['"' + c + '"' for c in target_champions]), len(target_champions))

    cursor.execute(query)

    column_names = [desc[0] for desc in cursor.description]

    df = pd.DataFrame(cursor.fetchall(), columns=column_names)

    df['champions'] = df['champions'].str.split(',')

    print(df)
    # df is in format match id, W, [champions]
    teammates = {}
    opponents = {}
    # iterate through rows of df
    for row_index, row in df.iterrows():
        if target_champions[0] in row[-1]:
            # iterate through teammate champions
            for champion in row[-1]:
                # champion name is key in dictionary champion : [wins, games played]
                value = teammates.get(champion, [0, 0])
                if 'W' == row[1]:
                    value[0] += 1
                value[1] += 1
                teammates[champion] = value
        else:
            # iterates through opponent champions, does same as above if statement
            for champion in row[-1]:
                value = opponents.get(champion, [0, 0])
                if 'W' == row[1]:
                    value[0] += 1
                value[1] += 1
                opponents[champion] = value

    # Create DataFrames for teammates and opponents from dictionaries
    rows_list = []
    for champion, stats in teammates.items():
        wins, games_played = stats
        win_ratio = wins / games_played if games_played != 0 else 0
        row_data = {'Champion': champion, 'Games Played': games_played, 'Wins': wins, 'Win Ratio': win_ratio}
        rows_list.append(row_data)
    teammate_df = pd.DataFrame(rows_list).sort_values(by='Win Ratio', ascending=False)

    rows_list = []
    for champion, stats in opponents.items():
        wins, games_played = stats
        win_ratio = wins / games_played if games_played != 0 else 0
        row_data = {'Champion': champion, 'Games Played': games_played, 'Wins': wins, 'Win Ratio': win_ratio}
        rows_list.append(row_data)
    opponent_df = pd.DataFrame(rows_list).sort_values(by='Win Ratio', ascending=False)

    # Print the DataFrame
    print(teammate_df)
    print(opponent_df)
