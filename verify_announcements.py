import sqlite3
import os

# Connect to the database
db_path = "d:/skillsprint/backend/app/skillsprint.db"
if not os.path.exists(db_path):
    print("Database not found at", db_path)
    exit()

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

def run_test():
    print("--- Verifying Database Schema ---")
    cursor.execute("PRAGMA table_info(users)")
    cols = [c[1] for c in cursor.fetchall()]
    print("User columns:", cols)
    
    expected_cols = ['role', 'mentor_id', 'child_id']
    all_present = True
    for col in expected_cols:
        if col in cols:
            print(f"[OK] column '{col}' present.")
        else:
            print(f"[FAIL] column '{col}' missing.")
            all_present = False

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='announcements'")
    if cursor.fetchone():
        print("[OK] Announcements table created.")
    else:
        print("[FAIL] Announcements table missing.")

    print("\n--- Verifying API Registration ---")
    with open("d:/skillsprint/backend/app/api/v1/api.py", "r") as f:
        content = f.read()
        if "announcements" in content:
            print("[OK] Announcements router registered.")
        else:
            print("[FAIL] Announcements router not found in api.py.")

run_test()
conn.close()
