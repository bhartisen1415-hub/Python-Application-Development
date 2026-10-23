import os
import sqlite3
from contextlib import closing

DB_PATH = os.getenv("DB_PATH", "items.db")


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with closing(get_connection()) as connection:
        with connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT NOT NULL DEFAULT '',
                    price REAL NOT NULL CHECK(price >= 0)
                )
            """)


def create_item(name, description, price):
    with closing(get_connection()) as connection:
        with connection:
            cursor = connection.execute(
                "INSERT INTO items (name, description, price) VALUES (?, ?, ?)",
                (name, description, price),
            )
            item_id = cursor.lastrowid
    return get_item(item_id)


def get_item(item_id):
    with closing(get_connection()) as connection:
        row = connection.execute(
            "SELECT * FROM items WHERE id = ?", (item_id,)
        ).fetchone()
    return dict(row) if row else None


def get_all_items():
    with closing(get_connection()) as connection:
        rows = connection.execute("SELECT * FROM items ORDER BY id").fetchall()
    return [dict(row) for row in rows]


def update_item(item_id, name, description, price):
    with closing(get_connection()) as connection:
        with connection:
            cursor = connection.execute(
                "UPDATE items SET name = ?, description = ?, price = ? WHERE id = ?",
                (name, description, price, item_id),
            )
            updated = cursor.rowcount > 0
    return get_item(item_id) if updated else None


def delete_item(item_id):
    with closing(get_connection()) as connection:
        with connection:
            cursor = connection.execute("DELETE FROM items WHERE id = ?", (item_id,))
            return cursor.rowcount > 0
