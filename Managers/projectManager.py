'''
File: projectManager.py
Project: Managers
File Created: Wednesday, 27th November 2024 1:28:03 pm
Author: Cortez L. McCrary (cortez.mccrary.codes@gmail.com)
-----
Last Modified: Sunday, 1st December 2024 9:33:19 am
Modified By: Cortez L. McCrary (cortez.mccrary.codes@gmail.com>)
-----
Copyright 2024 Cortez McCrary, Employee of JHU APL
'''

from typing import List
from rich import print
import typer
from dbController import add_project, get_projects, delete_project
from model import Budget, Project
from utils import create_table, display_menu, menu_selector, new_line, clear

def new_project_handler(title: str, description: str, budgets_str: str, owner: int):
    budgets: List[str] = budgets_str.split(',')
    title = add_project(title=title, description=description, budgets=budgets, user_id=owner)
    if title:
        print(f"[green]Project Added: {title}[/green]")
    else:
        print(f"[red]Adding project failed[/red]")

def print_project_table(user_id:int):
    '''
    Queries the database for all users 
    '''
    headers=["Project", "Description", "# of Budgets"]
    projects: Project = get_projects(user_id)
    rows: List[list] = []
    for project in projects:
        rows.append([project.title, project.description, str(len(project.budgets))])
    create_table(title="Projects", headers=headers, rows=rows)

def get_project_title_list(user_id:int):
    '''
    Returns a list of project titles.
    '''
    projects: List[Project] = get_projects(user_id=user_id)
    project_list: List[str] = []
    for project in projects:
        project_list.append(project.title)

    return project_list

def get_projects_list(user_id:int):
    return get_projects(user_id=user_id)

def print_project_list(project:Project):
    '''
    Displays details of a specific project
    '''
    print(f"[blue]Title:[/blue] {project.title}")
    print(f"[blue]description:[/blue] {project.description}")
    print(f"[blue]budgets:[/blue]")
    for budget in project.budgets:
        print(f"- {budget.budget_code}")

def delete_project_handler(user_id:int, project_id:int):
    '''
    Handles deleting projects based on id
    '''
    delete_project(user_id=user_id, project_id=project_id)
    