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
import time
from typing import List
from sqlalchemy.orm import Session
import typer
from Managers.projectManager import (print_project_list, print_project_table, new_project_handler, 
    get_project_title_list, get_projects_list, delete_project_handler)
from model import Project
from utils import create_confirmation, display_menu, get_confirmation, new_line, clear, optional_field_handler, menu_selector
from rich import print


def project_menu(user_id: int):
    '''
    Menu for Managing a User's Projects
    '''
    while True:
        print_project_table(user_id=user_id)
        display_menu(["View Project", "Add Project", "Delete Project", "Back to Main Menu"], "Project Menu")
        new_line()

        selection = menu_selector("Let's manage your Projects")

        match selection:
            case 1:
                view_project(user_id=user_id)
            case 2:
                clear()
                add_project_prompt(user_id=user_id)
                new_line()
            case 3:
                clear()
                delete_project_prompt(user_id=user_id)
            case 4:
                clear()
                break
            case -1:
                pass

def view_project(user_id:str):
    '''
    Prompts the user to select a project to view further details
    '''
    project_titles_list: List[str] = get_project_title_list(user_id=user_id)
    projects: List[Project] = get_projects_list(user_id=user_id)
 
    while True:
        clear()

        display_menu(title="Projects", options=project_titles_list)  
        new_line()
        selection = menu_selector("Select a project") 
        project = projects[selection-1] 
        new_line()
        print_project_list(project)
        new_line()
        continue_viewing = typer.confirm("Would you like to view another project")
        if not continue_viewing:
            break
    clear()

def add_project_prompt(user_id: int):
    '''
    Get's user responses for creating a new project. 
    '''
    # TODO ensure that when a project is created with at least one budget code
    while True:
        project_name = typer.prompt("Project Name")
        project_description = optional_field_handler(typer.prompt("Project Description", default="optional"))
        budgets = optional_field_handler(typer.prompt("Budget Codes (separate by commas)", default="optional"))
        clear()

        isConfirmed = get_confirmation([create_confirmation("Name", project_name),
                              create_confirmation("Description", project_description),
                              create_confirmation("Budgets", budgets)])
        if isConfirmed:
            new_project_handler(title=project_name, description=project_description, budgets_str=budgets, owner=user_id)
            break

def delete_project_prompt(user_id:int):
    '''
    Get's user responses for deleting a project and it's related budgets
    '''
    projects: List[Project] = get_projects_list(user_id=user_id)
    project_titles_list: List[str] = get_project_title_list(user_id=user_id)
    project_titles_list.append("Back to Project Menu")
    while True:
        display_menu(title="Projects", options=project_titles_list)  
        new_line()
        selection = menu_selector("Select a project to delete") 
        if selection == len(project_titles_list):
            clear()
            break
        project = projects[selection-1] 
        new_line()
        print_project_list(project)
        new_line()
        confirm_delete = typer.confirm(f"Confirm delete")
        if confirm_delete:
            clear()
            print(f"deleting {project.title}")
            delete_project_handler(user_id=user_id, project_id=project.id)
            time.sleep(1)
            clear()
            break

    clear()

def edit_project_prompt(user_id:int):
    '''
    Prompt for editing existing projects
    '''
    projects: List[Project] = get_projects_list(user_id=user_id)
    project_titles_list: List[str] = get_project_title_list(user_id=user_id)
    project_titles_list.append("Back to Project Menu")
    while True:
        display_menu(title="Projects", options=project_titles_list)  
        new_line()
        selection = menu_selector("Select a project to delete") 
        if selection == len(project_titles_list):
            clear()
            break
        project = projects[selection-1] 
        new_line()
        print_project_list(project)
        new_line()