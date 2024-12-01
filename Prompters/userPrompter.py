'''
File: userPrompter.py
Project: Prompters
File Created: Wednesday, 27th November 2024 2:27:37 pm
Author: Cortez L. McCrary (cortez.mccrary.codes@gmail.com)
-----
Last Modified: Wednesday, 27th November 2024 2:28:56 pm
Modified By: Cortez L. McCrary (cortez.mccrary.codes@gmail.com>)
-----
Copyright 2024 Cortez McCrary, Employee of JHU APL
'''

import time
from email_validator import EmailNotValidError
import typer
from os import system, name
from rich import print
from maskpass import advpass
from Managers.userManager import ConfirmPasswordError, WrongCredentialsError, register_user_handler, EmptyFieldError, login_handler
from sqlalchemy.exc import IntegrityError, DBAPIError, NoResultFound, MultipleResultsFound
from sqlalchemy.orm import Session

clear = lambda: system('cls' if name=='nt' else 'clear')

def login_prompt():
    '''
    Prompts for username and password to login to workcalc account
    '''
    clear()
    username = typer.prompt("Username")
    password = advpass()
    try:
        current_user = login_handler(username=username, password=password)
        clear()
        print(f"[green]Login successful![/green]")
        return current_user
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
                        confirmPassword=confirmPassword)
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
            clear()
            print(f"[green]Account created.[/green]")
            print(f"[green]Welcome, {firstName}![/green]")
            print(f"[green]Please login[/green]")
            time.sleep(1)
            clear()
        else:
            continue