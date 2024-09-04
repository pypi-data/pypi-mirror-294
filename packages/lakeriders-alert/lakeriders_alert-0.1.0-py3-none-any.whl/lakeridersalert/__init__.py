import sqlite3

from .constants import DB_NAME

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS calendar(
        datetime TEXT
        , members TEXT
    )
""")

conn.commit()
conn.close()
