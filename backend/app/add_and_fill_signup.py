import sqlite3, pathlib
p = pathlib.Path(r'd:\skillsprint\backend\app\skillsprint.db')
conn = sqlite3.connect(p)
try:
    conn.execute("ALTER TABLE users ADD COLUMN signup_date DATETIME")
    conn.commit()
    print('Added signup_date (no default)')
except Exception as e:
    print('ALTER failed:', e)
finally:
    conn.close()

conn = sqlite3.connect(p)
try:
    conn.execute("UPDATE users SET signup_date = datetime('now') WHERE signup_date IS NULL")
    conn.commit()
    print('Updated existing rows')
except Exception as e:
    print('UPDATE failed:', e)
finally:
    conn.close()
