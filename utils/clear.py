def clear():
    import os

    return os.system("cls" if os.name == "nt" else "clear")
