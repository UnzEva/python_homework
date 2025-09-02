import os
import sqlite3

def ensure_db_dir(db_dir: str) -> None:
    os.makedirs(db_dir, exist_ok=True)

def create_schema(conn: sqlite3.Connection) -> None:
    cursor = conn.cursor()
    statements = [
        """
        CREATE TABLE IF NOT EXISTS publishers (
            publisher_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name         TEXT NOT NULL UNIQUE
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS magazines (
            magazine_id  INTEGER PRIMARY KEY AUTOINCREMENT,
            name         TEXT NOT NULL UNIQUE,
            publisher_id INTEGER NOT NULL,
            FOREIGN KEY (publisher_id) REFERENCES publishers(publisher_id)
                ON DELETE CASCADE ON UPDATE CASCADE
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS subscribers (
            subscriber_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT NOT NULL,
            address       TEXT NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS subscriptions (
            subscription_id INTEGER PRIMARY KEY AUTOINCREMENT,
            subscriber_id   INTEGER NOT NULL,
            magazine_id     INTEGER NOT NULL,
            expiration_date TEXT    NOT NULL,
            FOREIGN KEY (subscriber_id) REFERENCES subscribers(subscriber_id)
                ON DELETE CASCADE ON UPDATE CASCADE,
            FOREIGN KEY (magazine_id)  REFERENCES magazines(magazine_id)
                ON DELETE CASCADE ON UPDATE CASCADE,
            UNIQUE (subscriber_id, magazine_id)
        );
        """
    ]
    for sql in statements:
        try:
            cursor.execute(sql)
        except sqlite3.Error as e:
            print(f"[ERROR] Failed to execute SQL:\n{sql}\nReason: {e}")
    try:
        conn.commit()
        print("[OK] Tables created (or already existed).")
    except sqlite3.Error as e:
        print(f"[ERROR] Commit failed: {e}")

# ---------- Insert helpers (de-dup safe) ----------

def add_publisher(conn: sqlite3.Connection, name: str) -> int | None:
    try:
        conn.execute("INSERT OR IGNORE INTO publishers(name) VALUES (?);", (name,))
        cur = conn.execute("SELECT publisher_id FROM publishers WHERE name = ?;", (name,))
        row = cur.fetchone()
        return row[0] if row else None
    except sqlite3.Error as e:
        print(f"[ERROR] add_publisher('{name}'): {e}")
        return None

def add_magazine(conn: sqlite3.Connection, name: str, publisher_name: str) -> int | None:
    try:
        pub_id = add_publisher(conn, publisher_name)
        if pub_id is None:
            return None
        conn.execute(
            "INSERT OR IGNORE INTO magazines(name, publisher_id) VALUES (?, ?);",
            (name, pub_id)
        )
        cur = conn.execute("SELECT magazine_id FROM magazines WHERE name = ?;", (name,))
        row = cur.fetchone()
        return row[0] if row else None
    except sqlite3.Error as e:
        print(f"[ERROR] add_magazine('{name}','{publisher_name}'): {e}")
        return None

def add_subscriber(conn: sqlite3.Connection, name: str, address: str) -> int | None:
    try:
        cur = conn.execute(
            "SELECT subscriber_id FROM subscribers WHERE name = ? AND address = ?;",
            (name, address)
        )
        row = cur.fetchone()
        if row:
            return row[0]
        conn.execute(
            "INSERT INTO subscribers(name, address) VALUES (?, ?);",
            (name, address)
        )
        cur = conn.execute(
            "SELECT subscriber_id FROM subscribers WHERE name = ? AND address = ?;",
            (name, address)
        )
        row = cur.fetchone()
        return row[0] if row else None
    except sqlite3.Error as e:
        print(f"[ERROR] add_subscriber('{name}','{address}'): {e}")
        return None

def add_subscription(conn: sqlite3.Connection,
                     sub_name: str, sub_address: str,
                     magazine_name: str, expiration_date: str) -> bool:
    try:
        sub_id = add_subscriber(conn, sub_name, sub_address)
        if sub_id is None:
            print(f"[WARN] Could not resolve subscriber '{sub_name}', '{sub_address}'.")
            return False
        cur = conn.execute("SELECT magazine_id FROM magazines WHERE name = ?;", (magazine_name,))
        row = cur.fetchone()
        if not row:
            print(f"[WARN] Magazine '{magazine_name}' does not exist; skipping subscription.")
            return False
        mag_id = row[0]
        conn.execute(
            "INSERT OR IGNORE INTO subscriptions(subscriber_id, magazine_id, expiration_date) VALUES (?,?,?);",
            (sub_id, mag_id, expiration_date)
        )
        return True
    except sqlite3.Error as e:
        print(f"[ERROR] add_subscription(...): {e}")
        return False

def populate_sample_data(conn: sqlite3.Connection) -> None:
    add_magazine(conn, "Tech Today",       "Acme Publishing")
    add_magazine(conn, "Healthy Life",     "Acme Publishing")
    add_magazine(conn, "Gardening Weekly", "Green Leaf Media")
    add_magazine(conn, "Travel World",     "Globe Press")
    add_magazine(conn, "Culinary Arts",    "Green Leaf Media")

    add_subscriber(conn, "Alice Johnson", "123 Maple St")
    add_subscriber(conn, "Bob Smith",     "456 Oak Ave")
    add_subscriber(conn, "Alice Johnson", "789 Pine Rd")
    add_subscriber(conn, "Carol Lee",     "222 Birch Blvd")

    add_subscription(conn, "Alice Johnson", "123 Maple St", "Tech Today",       "2025-12-31")
    add_subscription(conn, "Alice Johnson", "123 Maple St", "Healthy Life",     "2025-10-01")
    add_subscription(conn, "Bob Smith",     "456 Oak Ave",  "Gardening Weekly", "2026-01-15")
    add_subscription(conn, "Carol Lee",     "222 Birch Blvd","Travel World",    "2025-07-30")
    add_subscription(conn, "Alice Johnson", "789 Pine Rd",  "Culinary Arts",    "2025-03-10")

# ---------- Task 4: Queries ----------

def print_rows(title: str, rows) -> None:
    """Pretty-print rows from a SELECT. If row_factory is Row, print dicts for clarity."""
    print(f"\n=== {title} ===")
    for r in rows:
        try:
            print(dict(r))
        except Exception:
            print(r)

def run_task4_queries(conn: sqlite3.Connection) -> None:
    """
    1) Retrieve all info from subscribers
    2) Retrieve all magazines sorted by name
    3) Retrieve magazines for a particular publisher (JOIN)
    """
    try:
        cur = conn.execute("SELECT * FROM subscribers;")
        print_rows("All subscribers", cur.fetchall())

        cur = conn.execute("SELECT * FROM magazines ORDER BY name;")
        print_rows("Magazines (sorted by name)", cur.fetchall())

        publisher_name = "Acme Publishing"  
        sql = """
            SELECT m.magazine_id, m.name AS magazine_name, p.name AS publisher_name
            FROM magazines m
            JOIN publishers p ON m.publisher_id = p.publisher_id
            WHERE p.name = ?;
        """
        cur = conn.execute(sql, (publisher_name,))
        print_rows(f"Magazines published by '{publisher_name}'", cur.fetchall())

    except sqlite3.Error as e:
        print(f"[ERROR] SELECT failed: {e}")

# ---------- Main ----------

def main():
    base_dir = os.path.dirname(__file__)         
    db_dir = os.path.join(base_dir, "..", "db")   
    db_path = os.path.join(db_dir, "magazines.db")
    ensure_db_dir(db_dir)

    conn = None
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        # Task 3: enforce FK constraints
        conn.execute("PRAGMA foreign_keys = 1")
        print(f"[OK] Connected (FK ON) to: {os.path.abspath(db_path)}")

        # Task 2: schema
        create_schema(conn)

        # Task 3: populate data
        populate_sample_data(conn)
        conn.commit()
        print("[OK] Data populated and committed.")

        # Task 4: run the three queries and print all rows
        run_task4_queries(conn)

    except sqlite3.Error as e:
        print(f"[ERROR] SQLite operation failed: {e}")
    finally:
        if conn is not None:
            conn.close()
            print("[INFO] Connection closed.")

if __name__ == "__main__":
    main()