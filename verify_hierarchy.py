import sqlite3
import hashlib

def get_password_hash(password):
    # This is a dummy hash for verification seeding only. 
    # The app uses pbkdf2_sha256 naturally.
    return "dummy_hash" 

db_path = "d:/skillsprint/backend/app/skillsprint.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

def create_user(username, email, role, mentor_id=None, admin_id=None):
    try:
        cursor.execute(
            "INSERT INTO users (username, email, hashed_password, role, mentor_id, admin_id, xp, streak) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (username, email, "pbkdf2_sha256$600000$tS7N9x$dummy", role, mentor_id, admin_id, 100, 5)
        )
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        return cursor.fetchone()[0]

print("--- Seeding Hierarchical Data ---")

# 1. Create Admin
admin_id = create_user("superadmin", "admin@skillsprint.com", "admin")
print(f"Admin created: {admin_id}")

# 2. Create Mentor under Admin
mentor_id = create_user("pro_mentor", "mentor@skillsprint.com", "mentor", admin_id=admin_id)
print(f"Mentor created: {mentor_id}")

# 3. Create Student under Mentor
student_id = create_user("star_student", "student@skillsprint.com", "student", mentor_id=mentor_id)
print(f"Student created: {student_id}")

conn.commit()
conn.close()
print("Verification data seeded.")
