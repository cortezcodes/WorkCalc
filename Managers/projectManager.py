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
from dbController import add_project

def submit_new_project(title: str, description: str, owner: int):
    # try:
    title = add_project(title=title, description=description, user_id=owner)
    print(f"[green]Project Added: {title}[/green]")
    # except Exception as e: 
    #     print(f"[red]ERROR adding project:[/red] {e}")

    
    