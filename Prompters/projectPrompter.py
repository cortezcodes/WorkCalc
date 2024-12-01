'''
File: projectPrompter.py
Project: Prompters
File Created: Thursday, 28th November 2024 12:21:54 am
Author: Cortez L. McCrary (cortez.mccrary.codes@gmail.com)
-----
Last Modified: Thursday, 28th November 2024 12:22:46 am
Modified By: Cortez L. McCrary (cortez.mccrary.codes@gmail.com>)
-----
Copyright 2024 Cortez McCrary, Employee of JHU APL
'''
from sqlalchemy.orm import Session
import typer
from Managers.projectManager import print_project_table, submit_new_project
from utils import create_confirmation, display_menu, get_confirmation, new_line, clear, optional_field_handler
from rich import print


def project_menu(user_id: int):
    '''
    Menu for Managing a User's Projects
    '''
    while True:
        print_project_table(user_id=user_id)
        display_menu(["View Project", "Add Project", "Edit Project", "Delete Project", "Back"], "Project Menu")
        new_line()
        selection = int(typer.prompt("Let's manage your Projects"))

        match selection:
            case 1:
                clear()
                print("View Project Under Construction")
            case 2:
                clear()
                add_project_prompt(user_id=user_id)
                new_line()
            case 5:
                clear()
                break

def add_project_prompt(user_id: int):
    '''
    Get's user responses for creating a new project. 
    '''
    while True:
        project_name = typer.prompt("Project Name")
        project_description = optional_field_handler(typer.prompt("Project Description", default="optional"))
        budgets = optional_field_handler(typer.prompt("Budget Codes (separate by commas)", default="optional"))
        clear()

        isConfirmed = get_confirmation([create_confirmation("Name", project_name),
                              create_confirmation("Description", project_description),
                              create_confirmation("Budgets", budgets)])
        if isConfirmed:
            submit_new_project(title=project_name, description=project_description, budgets_str=budgets, owner=user_id)
            break
