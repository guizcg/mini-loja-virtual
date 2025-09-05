from utils import *
from .menu import *
from services import *


def run():
    clear()
    while True:
        main_menu()
        option = input("| > Opção: ")
        try:
            verify_option(option)
            match option:
                case "1":
                    login()
                case "2":
                    register()
                case "3":
                    clear()
                    break
                case _:
                    clear()
                    print("| R: Opcão Inválida.")
        except Exception as e:
            clear()
            print("| R: Erro Desconhecido.")
