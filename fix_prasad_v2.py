import sqlite3
import os

db_path = r"d:\skillsprint\backend\app\skillsprint.db"
conn = sqlite3.connect(db_path)
c = conn.cursor()

print("--- User Check: Dr prasad ---")
c.execute("SELECT id, username, role, join_code FROM users WHERE username = 'Dr prasad'")
row = c.fetchone()
print(f"Result: {row}")

if row and (not row[2] == 'admin' or not row[3]):
    print("Fixing user record...")
    c.execute("UPDATE users SET role='admin', join_code='ADM_DEBUG' WHERE username='Dr prasad'")
    conn.commit()
    print("User updated to admin with ADM_DEBUG code.")

conn.close()
