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
import typer
from rich import print
from utils import display_menu, new_line, clear
from model import User
from datetime import datetime
from Prompters.userPrompter import login_prompt, create_user_prompt
from Prompters.projectPrompter import project_menu
import time

current_user: User = None
current_date: datetime = datetime.now()


def main(): 
    clear()
    while True:
        display_menu(["login", "Create Account", "Exit"], title="Welcome to WorkCalc!")
        new_line()
        try:
            selection = int(typer.prompt("Make a selection"))
        except ValueError as e:
            new_line()
            print("[red]ERROR:[/red] Invalid input.")
            new_line()
            selection = -1
        
        match selection:
            case 1:
                global current_user
                current_user = login_prompt()
                if current_user != None:
                    main_menu()
            case 2:
                clear()
                create_user_prompt()
            case 3:
                clear()
                print("Goodbye")
                time.sleep(1)
                clear()
                break
            case -1:
                pass
            case _:
                print("[red]Invalid:[/red] Bad input, please try again.")

def main_menu():
    '''
    Display and controls UI interactions once a user has logged in. 
    '''
    formatted_date = current_date.strftime("%A, %d %B %Y")
    while True:
        display_menu(["Daily", "Manage Projects", "Logout"], f"Welcome, {current_user.first_name}\nDate: {formatted_date}")
        new_line()
        try:
            selection = int(typer.prompt("What would you like to do Today"))
        except ValueError as e:
            new_line()
            print("[red]ERROR:[/red] Invalid input.")
            new_line()
            selection = -1
        match selection:
            case 1:
                print("Daily is under construction")
            case 2:
                clear()
                project_menu(user_id=User.id)
            case 3:
                clear()
                print(f"Logging, {current_user.first_name} out. Goodbye!")
                current_user == None
                time.sleep(1)
                clear()
                break
            case -1:
                pass
            case _:
                print("[red]Invalid:[/red] Bad input, please try again.")


if __name__ == "__main__":
    typer.run(main)