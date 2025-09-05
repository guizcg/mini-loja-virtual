import sqlite3


def data():
    try:
        connection = sqlite3.connect("data/users.db")
        cursor = connection.cursor()
    except Exception:
        print("| R: Erro ao tentar se conectar com o banco de dados.")
        return
    try:
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            purchased_items TEXT,
            spent_value INTEGER DEFAULT 0
        )
    """
        )
        connection.commit()
        connection.close()
    except Exception:
        print("Erro na criação do banco de dados.")
        return
