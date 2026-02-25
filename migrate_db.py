import sqlite3

db_path = "d:/skillsprint/backend/app/skillsprint.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    print("Adding columns to 'users' table...")
    cursor.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'student'")
    cursor.execute("ALTER TABLE users ADD COLUMN mentor_id INTEGER")
    cursor.execute("ALTER TABLE users ADD COLUMN child_id INTEGER")
    print("Columns added successfully.")
except sqlite3.OperationalError as e:
    print(f"Note: {e}")

try:
    print("Creating 'announcements' table...")
    cursor.execute("""
    CREATE TABLE announcements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        mentor_id INTEGER,
        content TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(mentor_id) REFERENCES users(id)
    )
    """)
    print("Table created successfully.")
except sqlite3.OperationalError as e:
    print(f"Note: {e}")

conn.commit()
conn.close()
print("Migration complete.")
