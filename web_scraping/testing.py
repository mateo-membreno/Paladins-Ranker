import pandas as pd
import sqlite3 as sq

conn = sq.connect('paladins.db')
df = pd.read_sql_query('select * from match order by date', conn)
print(df)

1250519060
1250518428
1250513572

1250385789
