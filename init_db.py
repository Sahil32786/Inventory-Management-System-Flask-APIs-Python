import sqlite3
from pathlib import  Path
db_path = Path("data/products.db")
db_path.parent.mkdir(exist_ok=True)


conn = sqlite3.connect(db_path)

conn.execute("""
    CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    price REAL NOT NULL
    )
    """)
conn.commit()
print(f"db path {db_path.resolve()} ")