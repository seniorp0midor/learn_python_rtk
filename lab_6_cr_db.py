import pandas as pd
import sqlite3

data = pd.read_csv('Steam_2024_bestRevenue_1500.csv')
conn = sqlite3.connect('steam_database_lab_6.db')
data.to_sql('SteamData', conn, if_exists='replace', index=False)
cursor = conn.cursor()
cursor.execute("SELECT * FROM SteamData")
rows = cursor.fetchall()
for row in rows[:10]:
    print(row)

conn.close()

