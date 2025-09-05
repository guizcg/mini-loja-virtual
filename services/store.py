import sqlite3
import os
import ast
from .items import items as get_items
from controllers import *
from utils import *

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(base_dir, "data", "users.db")

connection = sqlite3.connect(db_path)
cursor = connection.cursor()

items = get_items()


def show_user_items(user_items, value):
    user_items_formatted = {}
    try:
        for item in user_items:
            counter = user_items.count(item)
            user_items_formatted[item] = counter

        for position, (item, quantity) in enumerate(
            user_items_formatted.items(), start=1
        ):
            print(f"| {position} - {item.capitalize()} {quantity}x")
        print("|")
        print(f"| R: Valor total: R${value}")
    except Exception:
        print("| R: Houve um erro.")


def store(user_name):
    user_items = []
    purchase_value = 0

    while True:
        option = input(
            """
[-------------- MINI LOJA VIRTUAL --------------]
|                                               |
|1 - Adicionar item ao carrinho                 |
|2 - Suas informações                           |
|3 - Voltar                                     |
[===============================================]
| > Opcão: """
        )
        verify_option(option)

        match option:
            case "1":
                try:
                    clear()
                    menu2(items)
                    print("\n[======================ITENS======================]")
                    show_user_items(user_items, purchase_value)

                    cursor.execute(
                        "SELECT purchased_items FROM users WHERE user_name = ?",
                        (user_name,),
                    )
                    verify_items = cursor.fetchone()[0]
                    purchased_items = []

                    if verify_items:
                        try:
                            purchased_items = ast.literal_eval(verify_items)
                        except Exception:
                            purchased_items = []

                    cursor.execute(
                        "SELECT spent_value FROM users WHERE user_name = ?",
                        (user_name,),
                    )
                    spent_value = cursor.fetchone()[0]

                    amount = input(
                        "| > Quantos itens você deseja adicionar ao carrinho?: "
                    )

                    if not amount.isnumeric():
                        clear()
                        print("| R: Apenas números inteiros.")
                        continue

                    amount = int(amount)
                    for number in range(amount):
                        chosen_item = input(f"| > Item {number + 1}: ").lower()
                        found = False

                        for category, item_dict in items.items():
                            if chosen_item in item_dict:
                                user_items.append(chosen_item)
                                purchase_value += item_dict[chosen_item]
                                found = True

                        if not found:
                            print(
                                f"| R: {chosen_item.capitalize()} não está disponível na loja."
                            )

                    print("\n[======================ITENS======================]")
                    show_user_items(user_items, purchase_value)

                except Exception:
                    print(
                        "| R: Houve um erro no sistema de adicionar items ao carrinho."
                    )

                if user_items:
                    while True:
                        menu3()
                        option = input("| > Opcão: ")

                        match option:
                            case "1":
                                try:
                                    clear()
                                    if not user_items:
                                        print("| R: Seu carrinho está vazio.")
                                        break

                                    if purchase_value > 500:
                                        print(
                                            "| R: Sua compra foi acima de R$500.00, desconto de R$50 aplicado!\n"
                                        )
                                        purchase_value -= 50
                                    elif purchase_value > 350:
                                        print(
                                            "| R: Mais de R$350.00 gastos! Desconto de R$25 aplicado.\n"
                                        )
                                        purchase_value -= 25
                                    elif purchase_value > 200:
                                        print(
                                            "| R: Mais de R$200.00 gastos! Desconto de R$15 aplicado.\n"
                                        )
                                        purchase_value -= 15

                                    spent_value += purchase_value
                                    for item in user_items:
                                        purchased_items.append(item)

                                    cursor.execute(
                                        "UPDATE users SET spent_value = ?, purchased_items = ? WHERE user_name = ?",
                                        (spent_value, str(purchased_items), user_name),
                                    )
                                    connection.commit()

                                    print(
                                        "[===============COMPRA FINALIZADA===============]"
                                    )
                                    show_user_items(user_items, purchase_value)
                                    print(
                                        "[===============================================]"
                                    )
                                    user_items = []
                                    purchase_value = 0
                                    break

                                except Exception:
                                    print("| R: Houve um erro no sistema de compras.")

                            case "2":
                                try:
                                    amount = input(
                                        "| > Quantos items você deseja remover do carrinho?: "
                                    )

                                    if not amount.isnumeric():
                                        clear()
                                        print("| R: Apenas números inteiros.")
                                        show_user_items(user_items, purchase_value)
                                        continue

                                    amount = int(amount)
                                    for number in range(amount):
                                        chosen_item = input(
                                            f"| > Item {number + 1}: "
                                        ).lower()
                                        found = False
                                        clear()
                                        if chosen_item in user_items:
                                            user_items.remove(chosen_item)
                                            for category, item_dict in items.items():
                                                if chosen_item in item_dict:
                                                    purchase_value -= item_dict[
                                                        chosen_item
                                                    ]
                                            print(
                                                f"| R: {chosen_item.capitalize()} foi removido do seu carrinho."
                                            )
                                            found = True

                                        if not found:
                                            print(
                                                f"| R: {chosen_item.capitalize()} não está no seu carrinho."
                                            )

                                    print(
                                        "\n[======================ITENS======================]"
                                    )
                                    if user_items:
                                        show_user_items(user_items, purchase_value)
                                    else:
                                        print("| > Seu carrinho está vazio.")
                                        break

                                except Exception:
                                    print(
                                        "| R: Houve um erro no sistema de remoção de items."
                                    )

                            case "3":
                                clear()
                                break
                            case _:
                                clear()
                                print("| R: Opcão Inválida.")
                                show_user_items(user_items, purchase_value)

            case "2":
                try:
                    cursor.execute(
                        "SELECT purchased_items FROM users WHERE user_name = ?",
                        (user_name,),
                    )
                    verify_items = cursor.fetchone()[0]
                    purchased_items = []
                    if verify_items:
                        try:
                            purchased_items = ast.literal_eval(verify_items)
                        except Exception:
                            purchased_items = []

                    cursor.execute(
                        "SELECT spent_value FROM users WHERE user_name = ?",
                        (user_name,),
                    )
                    spent_value = cursor.fetchone()[0]

                    cursor.execute(
                        "SELECT id FROM users WHERE user_name = ?",
                        (user_name,),
                    )
                    user_id = cursor.fetchone()[0]

                    clear()
                    print("[==================INFORMAÇÕES==================]\n|")
                    print(f"| Nome de Usuário: {user_name}\n| Id de Usuário: {user_id}")
                    print("|\n| Itens Comprados")
                    if purchased_items:
                        show_user_items(purchased_items, spent_value)
                    else:
                        print("| - Você ainda não realizou nenhuma compra.")
                    print("[===============================================]")

                except Exception:
                    print("| R: Houve um erro ao mostrar suas informações.")

            case "3":
                clear()
                return

            case _:
                clear()
                print("| R: Opcão Inválida.")
