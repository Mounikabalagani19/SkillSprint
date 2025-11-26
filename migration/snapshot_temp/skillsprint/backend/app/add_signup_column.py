import sqlite3, pathlib
db_path = r"d:\skillsprint\backend\app\skillsprint.db"
conn = sqlite3.connect(db_path)
try:
    conn.execute("ALTER TABLE users ADD COLUMN signup_date DATETIME DEFAULT (datetime('now'))")
    conn.commit()
    print("Added signup_date")
except Exception as e:
    print("ALTER failed:", e)
finally:
    conn.close()
