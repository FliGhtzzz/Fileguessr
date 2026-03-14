import sqlite3
import os

db_path = "file_guessr.db"

if os.path.exists(db_path):
    print(f"DB exists, size: {os.path.getsize(db_path)} bytes")
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM files")
        print(f"File count: {cursor.fetchone()[0]}")
        conn.close()
    except Exception as e:
        print(f"Error: {e}")
else:
    print("DB not found")
