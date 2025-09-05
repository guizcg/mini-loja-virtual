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
    for item in user_items:
        counter = user_items.count(item)
        user_items_formatted[item] = counter

    for position, (item, quantity) in enumerate(user_items_formatted.items(), start=1):
        print(f"| {position} - {item} {quantity}x")
    print("|")
    print(f"| R: Valor total: R${value}")


def store(user_name):
    while True:
        option = input(
            """
[-------------- MINI LOJA VIRTUAL --------------]
|1 - Loja                                       |
|2 - Suas informações                           |
|3 - Voltar                                     |
[===============================================]
| > Opcão: """
        )
        verify_option(option)

        match option:
            case "1":
                clear()
                menu2(items)
                try:
                    user_items = []

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

                    purchase_value = 0
                    amount = input(
                        "| > Quantos itens você deseja adicionar ao carrinho?: "
                    )
                    if amount.isnumeric():
                        amount = int(amount)
                        for number in range(amount):
                            chosen_item = input(f"| > Item {number + 1}: ").lower()
                            found = False

                            for category, item in items.items():
                                if chosen_item in item:
                                    user_items.append(chosen_item)
                                    purchase_value += item[chosen_item]
                                    found = True

                            if not found:
                                print(
                                    f"| R: {chosen_item.capitalize()} não está disponível na loja."
                                )

                        print("\n[======================ITENS======================]")
                        show_user_items(user_items, purchase_value)

                        if user_items:
                            while True:
                                option = input(
                                    """
[=================================================]
|1 - Concluir a compra                            |
|2 - Remover item do carrinho                     |
|3 - Sair                                         |
[=================================================]
| > Opcão: """
                                )
                                match option:
                                    case "1":
                                        clear()
                                        if not user_items:
                                            print("R: Seu carrinho está vazio.")
                                            break

                                        if purchase_value > 100:
                                            print(
                                                "| R: Sua compra foi acima do valor de R$100, você acaba de receber um desconto de R$15 no valor total da compra!\n"
                                            )
                                            purchase_value -= 15
                                        elif purchase_value > 50:
                                            print(
                                                "| R: Mais de R$50 gastos! Você acaba de receber um desconto de R$5 no valor total da sua compra.\n"
                                            )
                                            purchase_value -= 5

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
                                        break

                                    case "2":
                                        amount = input(
                                            "| > Quantos items você deseja remover do carrinho?: "
                                        )
                                        if amount.isnumeric():
                                            amount = int(amount)
                                            for number in range(amount):
                                                chosen_item = input(
                                                    f"| > Item {number + 1}: "
                                                ).lower()
                                                found = False
                                                clear()
                                                if chosen_item in user_items:
                                                    user_items.remove(chosen_item)
                                                    for category, item in items.items():
                                                        if chosen_item in item:
                                                            purchase_value -= item[chosen_item]
                                                    print(
                                                        f"| R: {chosen_item.capitalize()} foi removido do seu carrinho de compras."
                                                    )
                                                    found = True

                                                if not found:
                                                    print(
                                                        f"| R: {chosen_item.capitalize()} não está no seu carrinho."
                                                    )

                                            print("\n[======================ITENS======================]")
                                            if user_items:
                                                show_user_items(user_items, purchase_value)
                                            else:
                                                print("| > Seu carrinho esta vazio.")
                                                break
                                        else:
                                            clear()
                                            print("| R: Apenas números inteiros.")

                                            print("\n[======================ITENS======================]")
                                            show_user_items(user_items, purchase_value)

                                    case "3":
                                        clear()
                                        break
                                    case _:
                                        clear()
                                        print("| R: Opcão Inválida.")                                        
                                        print("\n[======================ITENS======================]")
                                        show_user_items(user_items, purchase_value)                                       
                    else:
                        clear()
                        print("| R: Apenas números inteiros.")

                except Exception:
                    clear()
                    print("| R: Houve um erro.")

            case "2":
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

            case "3":
                clear()
                return
            case _:
                print("| R: Opcão Inválida.")