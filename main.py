import typer # type: ignore
from os import system, name
import time

clear = lambda: system('cls' if name=='nt' else 'clear')

def displayMenu(options: list[str]):
    
    for option in options:
        print(f"{options.index(option)+1}) {option}")

def main():
    clear()
    while True:
        displayMenu(["login", "Create Account", "Exit"])
        selection = int(typer.prompt("Make selection"))
        
        match selection: # type: ignore
            case 1:
                clear()
                print("Loggin in\n")
            case 2:
                clear()
                print("Creating\n")
            case 3:
                clear()
                print("Goodbye")
                time.sleep(1)
                clear()
                break
            case _:
                print("invalid input, please try again.\n")


def login:
    

if __name__ == "__main__":
    print(name)
    typer.run(main)