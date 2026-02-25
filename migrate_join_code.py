import sqlite3

db_path = "d:/skillsprint/backend/app/skillsprint.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    print("Adding join_code to 'users' table...")
    cursor.execute("ALTER TABLE users ADD COLUMN join_code TEXT")
    print("Column added successfully.")
except sqlite3.OperationalError as e:
    print(f"Note (adding column): {e}")

try:
    print("Creating unique index on join_code...")
    cursor.execute("CREATE UNIQUE INDEX idx_join_code ON users(join_code)")
    print("Index created successfully.")
except sqlite3.OperationalError as e:
    print(f"Note (creating index): {e}")

conn.commit()
conn.close()
print("Migration complete.")
