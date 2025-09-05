import sqlite3
from .store import *
import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

db_path = os.path.join(base_dir, "data", "users.db")

connection = sqlite3.connect(db_path)
cursor = connection.cursor()


def login():
    try:
        user_name = input("| > Nome de Usuário: ")
        cursor.execute(
            "SELECT id, user_name FROM users WHERE user_name = ?", (user_name,)
        )
        user = cursor.fetchone()

        if user:
            cursor.execute(
                "SELECT password FROM users WHERE user_name = ?", (user_name,)
            )
            user_password = cursor.fetchone()
            password = input("| > Senha: ")
            if password in user_password:
                clear()
                store(user_name)
            else:
                print("| R: Senha incorreta.")
        else:
            res = input(
                "| R: Esse usuário não existe, deseja se cadastrar? [S/N]: "
            ).lower()
            if res == "s" or res == "sim" or res == "ss":
                register()
            else:
                return
    except Exception:
        print("| R: Houve um erro ao logar a conta.")


def register():
    try:
        user_name = input("| > Nome de usuário: ")
        cursor.execute("SELECT user_name FROM users WHERE user_name = ?", (user_name,))
        verify_user = cursor.fetchone()
        if verify_user:
            print("| R: Esse usuário já está registrado.")
        else:
            password = input("| > Senha: ")
            cursor.execute(
                "INSERT INTO users(user_name, password) VALUES (?,?)",
                (user_name, password),
            )
            connection.commit()
            clear()
            print("| R: Cadastro concluido com sucesso.")
    except Exception:
        print("| R: Houve um erro. Verifique suas informações de registro!")
