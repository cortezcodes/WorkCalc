'''
File: main.py
Project: WorkCalc
File Created: Friday, 22nd November 2024 8:22:26 pm
Author: Cortez L. McCrary (cortez.mccrary.codes@gmail.com)
-----
Last Modified: Saturday, 23rd November 2024 4:17:02 pm
Modified By: Cortez L. McCrary (cortez.mccrary.codes@gmail.com>)
-----
Copyright 2024 Cortez McCrary, Employee of JHU APL
'''

from email_validator import EmailNotValidError
import typer
from os import system, name
from rich import print
from maskpass import advpass
from dbController import startConnection
from userManagement import ConfirmPasswordError, WrongCredentialsError, register_user_handler, EmptyFieldError, login_handler
from sqlalchemy.exc import IntegrityError, DBAPIError, NoResultFound, MultipleResultsFound
import time



clear = lambda: system('cls' if name=='nt' else 'clear')
session = startConnection()



def display_menu(options: list[str], title=""):
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
        display_menu(["login", "Create Account", "Exit"], title="Welcome to WorkCalc!")
        selection = int(typer.prompt("Make selection"))
        
        match selection:
            case 1:
                login_prompt()    
            case 2:
                clear()
                create_user_prompt()
            case 3:
                clear()
                print("Goodbye")
                time.sleep(1)
                clear()
                break
            case _:
                print("invalid input, please try again.\n")


def login_prompt():
    '''
    Prompts for username and password to login to workcalc account
    '''
    clear()
    username = typer.prompt("Username")
    password = advpass()
    try:
        user = login_handler(username=username, password=password, session=session)
        print(f"[green]Login successful. Welcome, {user.first_name}![/green]")
    except EmptyFieldError as e:
        print(f"[red]{e}[/red]\n")
    except NoResultFound as e:
        print(f"[red]Username and/or password incorrect[/red]")
    except MultipleResultsFound as e:
        print("Unexpected error, multiple results found")
    except WrongCredentialsError as e:
        print(f"[red]{e}[/red]")

    


def create_user_prompt():
    '''
    Menu for creating a new user
    '''
    isCreated = False
    clear()
    while not isCreated:
        
        print("Create new account:\n")
        firstName = typer.prompt("First Name")
        lastName = typer.prompt("Last Name")
        email = typer.prompt("Email")
        username = typer.prompt("Username")
        password = advpass()
        confirmPassword = advpass(prompt="Confirm Password:")

        clear()
        print(f"Name: {firstName} {lastName}")
        print(f"Email: {email}")
        print(f"username: {username}")

        isConfirmed = typer.confirm("Confirm information")
        if isConfirmed:
            try:
                register_user_handler(firstName=firstName, 
                        lastName=lastName, 
                        email=email, 
                        username=username, 
                        password=password, 
                        confirmPassword=confirmPassword,
                        session=session)
            except EmailNotValidError as e:
                print("[red]Email was not valid, please try again![/red]")
                continue
            except (IntegrityError, DBAPIError, TypeError) as e:
                print("[red]Either email or username is not unique")
                continue
            except ConfirmPasswordError as e:
                print(f"[red]{e}[/red]")
                continue
            except Exception as e:
                print(type(e))
                print(f"[red]An unexpected error occurred:[/red] {e}")
                continue

            isCreated = True
            print(f"[green]Account created.[/green]")
            print(f"[green]Welcome, {firstName}![/green]")
            print(f"[green]Please login[/green]")
        else:
            continue

if __name__ == "__main__":
    typer.run(main)