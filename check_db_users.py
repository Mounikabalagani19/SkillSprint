import sqlite3

db_path = "d:/skillsprint/backend/app/skillsprint.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT id, username, role, join_code, admin_id, mentor_id FROM users")
users = cursor.fetchall()

print(f"{'ID':<4} | {'Username':<15} | {'Role':<10} | {'Join Code':<10} | {'Admin':<5} | {'Mentor':<5}")
print("-" * 65)
for u in users:
    print(f"{u[0]:<4} | {u[1]:<15} | {u[2]:<10} | {str(u[3]):<10} | {str(u[4]):<5} | {str(u[5]):<5}")

conn.close()
