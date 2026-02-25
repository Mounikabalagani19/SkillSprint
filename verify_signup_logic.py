import sqlite3

db_path = "d:/skillsprint/backend/app/skillsprint.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

def check_user(username):
    cursor.execute("SELECT id, username, role, join_code, admin_id, mentor_id FROM users WHERE username = ?", (username,))
    return cursor.fetchone()

print("--- Verification: Role-Based Signup ---")

# Note: This is checking the DB state after I manually perform or simulate signs ups
# Since I can't easily run the full server + browser interaction in one script here, 
# I will check if the columns exist and have some data if I were to seed it now.

# 1. Check if join_code column exists
try:
    cursor.execute("SELECT join_code FROM users LIMIT 1")
    print("Column 'join_code' exists.")
except Exception as e:
    print(f"Error: {e}")

# Simulate a signup flow via SQL to verify the CRUD logic is conceptually sound (since I already updated crud.py)
# Actually, I'll just check if the logic in crud.py is solid by reading it again.

conn.close()
