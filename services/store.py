import sqlite3
import os
import ast
from utils import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(BASE_DIR, "data", "users.db")

connection = sqlite3.connect(db_path)
cursor = connection.cursor()

items = {
    "alimentos": {"hotdog": 20, "batata": 10, "carne": 30, "salada": 5},
    "bebidas": {"coca-cola": 12, "fanta": 12, "suco tang": 2},
}


def menu2():
    print("[--------------- MINI LOJA VIRTUAL ---------------]")
    print("[------------------ PRODUTOS ---------------------]")

    for category, product in items.items():
        print("[=================================================]")
        print(f"[{category.upper():^49}]")
        print("[=================================================]")
        for item, value in product.items():
            print(f"| {item.capitalize():<25} - R${value:.2f}")
    print("[=================================================]")


def store(user_name):
    while True:
        option = input(
            """
[-------------- MINI LOJA VIRTUAL --------------]
|1 - Loja                                       |
|2 - Suas informações                           |
|3 - Voltar                                     |
[===============================================]
> Opcão: """
        )
        verify_option(option)

        match option:
            case "1":
                clear()
                menu2()
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
                        "> Quantos itens você deseja adicionar ao carrinho?: "
                    )
                    if amount.isnumeric():
                        amount = int(amount)
                        for number in range(amount):
                            chosen_item = input(f"> Item {number + 1}: ").lower()
                            found = False

                            for category, item in items.items():
                                if chosen_item in item:
                                    user_items.append(chosen_item)
                                    purchase_value += item[chosen_item]
                                    found = True

                            if not found:
                                print(
                                    f"R: {chosen_item.capitalize()} não está disponível na loja."
                                )

                        print("\n[======================ITENS======================]")
                        for item in user_items:
                            print(f"-> {item}")
                        print(f"R: Valor total no carrinho: R${purchase_value}")

                        if user_items:
                            while True:
                                option = input(
                                    """
[=================================================]
|1 - Concluir a compra                            |
|2 - Remover item do carrinho                     |
|3 - Sair                                         |
[=================================================]
> Opcão: """
                                )
                                match option:
                                    case "1":
                                        if not user_items:
                                            print("R: Seu carrinho está vazio.")
                                            break

                                        if purchase_value > 100:
                                            print(
                                                "R: Sua compra foi acima do valor de R$100, você acaba de receber um desconto de R$15 no valor total da compra!"
                                            )
                                            purchase_value -= 15
                                        elif purchase_value > 50:
                                            print(
                                                "Mais de R$50 gastos! Você acaba de receber um desconto de R$5 no valor total da sua compra."
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
                                        clear()
                                        print(
                                            "[==================COMPRA FINALIZADA!=================]"
                                        )
                                        print(f"R: Valor Total: R${purchase_value}")
                                        print(
                                            "[===============================================]"
                                        )
                                        
                                        break

                                    case "2":
                                        amount = input(
                                            "> Quantos items você deseja remover do carrinho?: "
                                        )
                                        if amount.isnumeric():
                                            amount = int(amount)
                                            for number in range(amount):
                                                chosen_item = input(
                                                    f"> Item {number + 1}: "
                                                ).lower()
                                                found = False

                                                if chosen_item in user_items:
                                                    user_items.remove(chosen_item)
                                                    for category, item in items.items():
                                                        if chosen_item in item:
                                                            purchase_value -= item[chosen_item]
                                                    print(
                                                        f"R: {chosen_item.capitalize()} foi removido do seu carrinho de compras."
                                                    )
                                                    found = True

                                                if not found:
                                                    print(
                                                        f"R: {chosen_item.capitalize()} não está no seu carrinho."
                                                    )

                                            print("\n[======================ITENS======================]")
                                            for item in user_items:
                                                print(f"-> {item}")
                                            print(
                                                f"R: Valor total no carrinho: R${purchase_value}"
                                            )
                                        else:
                                            print("Apenas números inteiros.")

                                    case "3":
                                        break
                                    case _:
                                        print("R: Opcão Inválida.")
                    else:
                        print("R: Apenas números inteiros.")

                except Exception:
                    print("R: Houve um erro.")
                    
            case "2":
              cursor.execute("SELECT purchased_items FROM users WHERE user_name = ?", (user_name,))
              verify_items = cursor.fetchone()[0]
              purchased_items = []
              if verify_items:
                try:
                  purchased_items = ast.literal_eval(verify_items)
                except Exception:
                  purchased_items = []
              cursor.execute("SELECT spent_value FROM users WHERE user_name = ?", (user_name,))
              spent_value = cursor.fetchone()[0]
              cursor.execute("SELECT id FROM users WHERE user_name = ?", (user_name,))
              user_id = cursor.fetchone()[0]
              print("[==================INFORMAÇÕES==================]\n|")
              print(f"| Nome de Usuário: {user_name}\n| Id de Usuário: {user_id}")
              print("|\n| Itens Comprados")
              for item in purchased_items:
                print(f'| -> {item}')
              print(f"|\n| VALOR TOTAL JÁ GASTO\n| -> R${spent_value}")
              print("[===============================================]")
              
                  
            case "3":
                return
            case _:
                print("R: Opcão Inválida.")