import typer
from os import system, name
from rich import print
from rich.console import Console
from maskpass import advpass
from dbController import startConnection, isUserNameFree
from email_validator import validate_email, EmailNotValidError
import time


clear = lambda: system('cls' if name=='nt' else 'clear')
session = startConnection()

def displayMenu(options: list[str], title=""):
    '''
    Helper function for displaying a terminal menu, providing auto numbering and optional title\n
    options: list[str] - each string within the list will become an option in the terminal menu\n
    title: str (optional) - creates a title for the terminal menu\n
    '''
    if title != "":
        print(title)

    for option in options:
        print(f"{options.index(option)+1}) {option}")

def main():
    
    clear()
    while True:
        displayMenu(["login", "Create Account", "Exit"], title="Welcome to WorkCalc!")
        selection = int(typer.prompt("Make selection"))
        
        match selection:
            case 1:
                login()    
            case 2:
                clear()
                createUser()
            case 3:
                clear()
                print("Goodbye")
                time.sleep(1)
                clear()
                break
            case _:
                print("invalid input, please try again.\n")


def login():
    '''
    Prompts for username and password to login to workcalc account
    '''
    
    username = typer.prompt("Username")
    password = advpass()

def createUser():
    '''
    Prompts creating a new user 
    '''
    print("Create new account:\n")
    isValidEmail = False
    isUniqueUsername = False
    isConfirmedPassword = False

    # Prompts to the user
    firstName = typer.prompt("First Name")
    lastName = typer.prompt("Last Name")
    while not isValidEmail:
        try:
            email = validate_email(typer.prompt("Email")).email
            isValidEmail = True
        except EmailNotValidError as e:
            print("[red]Email was not valid, please try again![/red]")

    while not isUniqueUsername:
        username = typer.prompt("Username")
        isUniqueUsername = isUserNameFree(username, session)
        if isUniqueUsername:
            print("[green]Username is available[/green]")
        else:
            print("[red]username already taken please try again")
    
    while not isConfirmedPassword:
        password = advpass()
        confirmPassword = advpass(prompt="Confirm Password:")
        if password == confirmPassword:
            isConfirmedPassword = True
        else:
            print("[red]Password did not match! Please try again.[/red]")

        
    #TODO Confirm all information before submitting to the db
    #TODO Confirm a username does not already exist


    

if __name__ == "__main__":
    typer.run(main)