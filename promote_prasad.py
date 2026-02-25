import sqlite3
import random
import string

def generate_code(length=8):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

db_path = r"d:\skillsprint\backend\app\skillsprint.db"
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Promote Dr prasad
code = "ADM_" + generate_code(5)
c.execute("UPDATE users SET role = 'admin', join_code = ? WHERE username = 'Dr prasad'", (code,))
conn.commit()

c.execute("SELECT username, role, join_code FROM users WHERE username = 'Dr prasad'")
print(f"Update result: {c.fetchone()}")

conn.close()
