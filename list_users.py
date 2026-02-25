import sqlite3

db_path = r"d:\skillsprint\backend\app\skillsprint.db"
conn = sqlite3.connect(db_path)
c = conn.cursor()

print("--- Listing All Users ---")
c.execute("SELECT id, username, role, join_code FROM users")
for row in c.fetchall():
    print(f"ID: {row[0]} | Username: [{row[1]}] | Role: {row[2]} | Code: {row[3]}")

conn.close()
