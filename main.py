from functions_updating import establish_db_connection
from functions_query import best_picks_given



if __name__ == "__main__":
        
    conn = establish_db_connection()
    cursor = conn.cursor()

    best_picks_given(["Inara", "Grover"], cursor)


