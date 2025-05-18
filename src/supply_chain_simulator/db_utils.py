# src/db_utils.py

import sqlite3


def save_to_sqlite(db_path, tables: dict):
    conn = sqlite3.connect(db_path)
    for name, df in tables.items():
        df.to_sql(name, conn, if_exists="replace", index=False)
    conn.commit()
    conn.close()
    print(f"Saved SQLite DB: {db_path}")
