import sqlite3
from .store import *

path = "data/users.db"
connection = sqlite3.connect(path)
cursor = connection.cursor()


def login():
    try:
        user_name = input("> Nome de Usuário: ")
        cursor.execute(
            "SELECT id, user_name FROM users WHERE user_name = ?", (user_name,)
        )
        user = cursor.fetchone()

        if user:
            cursor.execute(
                "SELECT password FROM users WHERE user_name = ?", (user_name,)
            )
            user_password = cursor.fetchone()
            password = input("> Senha: ")
            if password in user_password:
                print("R: Sucesso no Login.")
                store(user_name)
            else:
                print("R: Senha incorreta.")
        else:
            res = input(
                "R: Esse usuário não existe, deseja se cadastrar? [S/N]: "
            ).lower()
            if res == "s" or res == "sim" or res == "ss":
                register()
            else:
                return
    except Exception:
        print("R: Houve um erro. Verifique suas informações!")


def register():
    try:
        user_name = input("> Nome de usuário: ")
        cursor.execute("SELECT user_name FROM users WHERE user_name = ?", (user_name,))
        verify_user = cursor.fetchone()
        if verify_user:
            print("R: Esse usuário já está registrado.")
        else:
            password = input("> Senha: ")
            cursor.execute(
                "INSERT INTO users(user_name, password) VALUES (?,?)",
                (user_name, password),
            )
            connection.commit()
            print("R: Cadastro concluido com sucesso.")
    except Exception:
        print("R: Houve um erro. Verifique suas informações!")
