from controllers import run
from data import data

if __name__ == "__main__":
    try:
        data()
        run()
    except Exception as e:
        print("R: Erro ao iniciar o programa: \n", e)
