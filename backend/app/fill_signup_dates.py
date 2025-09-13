import sqlite3, pathlib
db_path = r"d:\skillsprint\backend\app\skillsprint.db"
conn = sqlite3.connect(db_path)
conn.execute("UPDATE users SET signup_date = datetime('now') WHERE signup_date IS NULL")
conn.commit()
conn.close()
print("Updated existing rows")
