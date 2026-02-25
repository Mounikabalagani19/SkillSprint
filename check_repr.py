import sqlite3

db_path = r"d:\skillsprint\backend\app\skillsprint.db"
conn = sqlite3.connect(db_path)
c = conn.cursor()

c.execute("SELECT username, role, join_code FROM users WHERE username = 'Dr prasad'")
row = c.fetchone()
print(f"Full Row: {repr(row)}")

conn.close()
