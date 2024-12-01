'''
File: projectManagement.py
Project: WorkCalc
File Created: Wednesday, 27th November 2024 1:28:03 pm
Author: Cortez L. McCrary (cortez.mccrary.codes@gmail.com)
-----
Last Modified: Wednesday, 27th November 2024 2:07:34 pm
Modified By: Cortez L. McCrary (cortez.mccrary.codes@gmail.com>)
-----
Copyright 2024 Cortez McCrary, Employee of JHU APL
'''


from typing import List
from rich import print
from dbController import add_project, get_projects
from model import Project
from utils import create_table

def submit_new_project(title: str, description: str, budgets_str: str, owner: int):
    budgets: List[str] = budgets_str.split(',')
    title = add_project(title=title, description=description, budgets=budgets, user_id=owner)
    if title:
        print(f"[green]Project Added: {title}[/green]")
    else:
        print(f"[red]Adding project failed[/red]")

def print_project_table(user_id:str):
    '''
    Queries the database for all users 
    '''
    headers=["Project", "Description", "# of Budgets"]
    projects: Project = get_projects(user_id)
    rows: List[list] = []
    for project in projects:
        rows.append([project.title, project.description, str(len(project.budgets))])
    create_table(title="Projects", headers=headers, rows=rows)

    
    