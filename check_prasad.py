import sqlite3
import os

db_path = r"d:\skillsprint\backend\app\skillsprint.db"
if not os.path.exists(db_path):
    print(f"DB not found at {db_path}")
    exit(1)

conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute("SELECT username, role, join_code FROM users WHERE username LIKE '%prasad%'")
results = c.fetchall()
print(f"Search results for 'prasad': {results}")
conn.close()
