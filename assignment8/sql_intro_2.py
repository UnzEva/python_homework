import os
import sqlite3
import pandas as pd

BASE_DIR = os.path.dirname(__file__)   
DB_DIR   = os.path.join(BASE_DIR, "..", "db")
DB_PATH  = os.path.join(DB_DIR, "lesson.db")
CSV_OUT  = os.path.join(BASE_DIR, "order_summary.csv")

def main():
    sql = """
        SELECT
            li.line_item_id,
            li.quantity,
            p.product_id,
            p.product_name,
            p.price
        FROM line_items AS li
        JOIN products AS p
             ON li.product_id = p.product_id;
    """

    # Check that the database exists
    if not os.path.exists(DB_PATH):
        print(f"[ERROR] Cannot find {os.path.abspath(DB_PATH)}.")
        print("Run load_db.py from the repository root to create ../db/lesson.db, then try again.")
        return

    # Read SQL directly into a DataFrame
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql_query(sql, conn)

    print("First 5 rows (raw JOIN):")
    print(df.head())

    # Add 'total' = quantity * price
    df["total"] = df["quantity"] * df["price"]

    print("\nFirst 5 rows (with 'total'):")
    print(df.head())

    # Group by product_id with required aggregations
    summary = (
        df.groupby("product_id", as_index=False)
          .agg(
              line_item_id=("line_item_id", "count"), 
              total=("total", "sum"),                  
              product_name=("product_name", "first")   
          )
          .sort_values(by="product_name", kind="mergesort")
          .reset_index(drop=True)
    )

    print("\nFirst 5 rows (grouped & sorted):")
    print(summary.head())

    summary.to_csv(CSV_OUT, index=False)
    print(f"\n[OK] Wrote summary to: {os.path.abspath(CSV_OUT)}")

if __name__ == "__main__":
    main()