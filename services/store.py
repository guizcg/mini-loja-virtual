import sqlite3
from utils import *

connection = sqlite3.connect("data/users.db")
cursor = connection.cursor()

products = {
    "alimentos": {"hotdog": 20, "batata": 10, "carne": 30, "salada": 5},
    "bebidas": {"coca-cola": 12, "fanta": 12, "suco tang": 2},
}


def menu2():
    print("[--------------- MINI LOJA VIRTUAL ---------------]")
    print("[------------------ PRODUTOS ---------------------]")

    for category, item in products.items():
        print("[=================================================]")
        print(f"[{category.upper():^49}]")
        print("[=================================================]")
        for product, value in item.items():
            print(f"| {product.capitalize():<25} - R${value:.2f}")
    print("[=================================================]")


def store(user_name):
    while True:
        option = input(
            """
[===============================================]
|1 - Loja                                       |
|2 - Voltar                                     |
[===============================================]
> Opcão: """
        )
        verify_option(option)
        match option:
            case "1":
                clear()
                menu2()
                try:
                    user_products = []
                    cursor.execute(
                        "SELECT total_value FROM users WHERE user_name = ?",
                        (user_name,),
                    )
                    total_value = cursor.fetchone()[0]
                    buy = 0
                    amount = input(
                        "Quantos produtos você deseja adicionar ao carrinho?: "
                    )
                    if amount.isnumeric():
                        amount = int(amount)
                        for number in range(amount):
                            user_product = input(f"Produto {number + 1}: ").lower()
                            found = False

                            for category, item in products.items():
                                if user_product in item:
                                    user_products.append(user_product)
                                    buy += item[user_product]
                                    found = True

                            if not found:
                                print(
                                    f"R: {user_product.capitalize()} não está disponível no nosso estoque."
                                )

                        print("\n\n[===============================================]")
                        print("---------------------CARRINHO--------------------")
                        for product in user_products:
                            print(f"-> {product}")
                        print(f"R: Valor: R${buy}")

                        if user_products:
                          while True:
                            print("\n\n[===============================================]")
                            print("---------------------CARRINHO--------------------")
                            for product in user_products:
                               print(f"-> {product}")
                            print(f"R: Valor: R${buy}")                           
                            option = input(
                                """
[===============================================]                            
|1 - Comprar                                    |
|2 - Remover item do carrinho                   |
|3 - Voltar                                     |
[===============================================]
> Opcão: """
                            )
                            match option:
                                case "1":
                                    if buy > 100:
                                        print(
                                            "Mais de R$100 gastos! Você acaba de receber um desconto de R$15 no valor total da sua compra."
                                        )
                                        buy -= 15
                                    elif buy > 50:
                                        print(
                                            "Mais de R$50 gastos! Você acaba de receber um desconto de R$5 no valor total da sua compra."
                                        )
                                        buy -= 5

                                    total_value += buy
                                    print(
                                        "[========================COMPRA CONCLUIDA=======================]"
                                    )
                                    print(f"R: Valor Total: R${buy}")
                                    print(
                                        "[===============================================]"
                                    )

                                    cursor.execute(
                                        "UPDATE users SET total_value = ?, products = ? WHERE user_name = ?",
                                        (total_value, str(user_products), user_name),
                                    )
                                    connection.commit()

                                case "2":
                                    amount = input(
                                        "> Quantos items você deseja remover do carrinho?: "
                                    )
                                    if amount.isnumeric():
                                        amount = int(amount)
                                        for i in range(amount):
                                            user_product = input(
                                                f"Item {i + 1}: "
                                            ).lower()
                                            found = False

                                            if user_product in user_products:
                                                user_products.remove(user_product)
                                                for category, item in products.items():
                                                    if user_product in item:
                                                        buy -= item[user_product]
                                                print(
                                                    f"R: {user_product.capitalize()} foi removido do seu carrinho de compras."
                                                )
                                                found = True

                                            if not found:
                                                print(
                                                    f"R: {user_product.capitalize()} não está no seu carrinho."
                                                )

                                        print(
                                            "\n\n[===============================================]"
                                        )
                                        print(
                                            "---------------------CARRINHO---------------------"
                                        )
                                        for product in user_products:
                                            print(f"-> {product}")
                                        print(f"R: Valor no carrinho: R${buy}")
                                      

                                    else:
                                        
                                        print("Apenas números inteiros.")
                                case "3":
                                  break
                                case _:
                                    
                                    print("R: Opcão Inválida.")

                    else:
                        
                        print("Apenas números inteiros.")

                except Exception as e:
                    print("R: Houve um erro.")

            case "2":
                return
            case _:
                print("R: Opcão Inválida.")
