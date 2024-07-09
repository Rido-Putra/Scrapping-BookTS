import sqlite3


def opening():
    """Display welcome message."""
    print("------------------------------------------")
    print("Hello, Welcome to scrapping project!")
    print("------------------------------------------")
    return


def save_to_sqlite(data):
    # membuat koneksi ke database(atau mebuat database jika belum ada)
    conn = sqlite3.connect("products.db")
    cursor = conn.cursor()

    # membuat tabel jika belum ada
    cursor.execute(
        """
                      CREATE TABLE IF NOT EXISTS products (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      title TEXT,
                      price REAL,
                      stock_availability INTEGER,
                      product_description TExt)"""
    )

    # memasukan data dari dictionary ke dalam tabel
    for product in data:
        cursor.execute(
            """INSERT INTO products (title, price, stock_availability, product_description)
                          VALUES (?, ?, ?, ?)""",
            (
                product["title"],
                product["price"],
                product["stock availability"],
                product["product description"],
            ),
        )

    # menyimpan perubahan dan menutup koneksi
    conn.commit()
    conn.close()
