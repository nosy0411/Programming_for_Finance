import pandas as pd
import sqlite3

# SQLite3 DB 불러오기
con = sqlite3.connect("종목가격정보.db")
df = pd.read_sql("SELECT * FROM '000040'", con)
con.close()

print(df.head(10))