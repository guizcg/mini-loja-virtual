def main_menu():
    print(
        """
[---------------MINI LOJA VIRTUAL---------------]
[===============================================]
[                                               ]
|1 - Login                                      |
|2 - Registrar novo usuário                     |
|3 - Sair                                       |
[===============================================]"""
    ) 

def menu2(items):
    print("[--------------- MINI LOJA VIRTUAL ---------------]")

    for category, product in items.items():
        print("[=================================================]")
        print(f"[{category.upper():^49}]")
        print("[=================================================]")
        for item, value in product.items():
            print(f"| {item.capitalize():<25} - R${value:.2f}")
    print("[=================================================]")