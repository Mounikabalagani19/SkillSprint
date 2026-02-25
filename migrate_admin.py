import sqlite3

db_path = "d:/skillsprint/backend/app/skillsprint.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    print("Adding admin_id to 'users' table...")
    cursor.execute("ALTER TABLE users ADD COLUMN admin_id INTEGER")
    print("Column added successfully.")
except sqlite3.OperationalError as e:
    print(f"Note: {e}")

conn.commit()
conn.close()
print("Migration complete.")
