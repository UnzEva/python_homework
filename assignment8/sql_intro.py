# Task 1: Connect to a new SQLite database and close the connection safely.
import os
import sqlite3

def main():
    # Build ../db/magazines.db relative to this file
    base_dir = os.path.dirname(__file__)                 # assignment8/
    db_dir = os.path.join(base_dir, "..", "db")          # ../db
    db_path = os.path.join(db_dir, "magazines.db")       # ../db/magazines.db

    # Ensure ../db exists
    os.makedirs(db_dir, exist_ok=True)

    conn = None
    try:
        # Connect will create the file if it does not exist
        conn = sqlite3.connect(db_path)
        print(f"[OK] Connected to: {os.path.abspath(db_path)}")
        # (No SQL statements yet in Task 1; just testing the connection.)
    except sqlite3.Error as e:
        # Any SQL-related error would be caught here
        print(f"[ERROR] SQLite connection failed: {e}")
    finally:
        # Always close the connection if it was opened
        if conn is not None:
            conn.close()
            print("[INFO] Connection closed.")

if __name__ == "__main__":
    main()