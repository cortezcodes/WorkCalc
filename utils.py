'''
File: utils.py
Project: WorkCalc
File Created: Thursday, 28th November 2024 12:27:46 am
Author: Cortez L. McCrary (cortez.mccrary.codes@gmail.com)
-----
Last Modified: Thursday, 28th November 2024 12:28:04 am
Modified By: Cortez L. McCrary (cortez.mccrary.codes@gmail.com>)
-----
Copyright 2024 Cortez McCrary, Employee of JHU APL
'''
from os import system, name
from typing import List
from rich import print
import typer

clear = lambda: system('cls' if name=='nt' else 'clear')
new_line = lambda: print("\n")

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

def create_confirmation(title: str, value: str):
    return {"Title": title, "Value": value}

def get_confirmation(fields: List[dict]):
    '''
    Used to display a list and request the user confirm the values\n
    fields: List[{"Title": "", "Value": ""}]
    returns True if confirmed or False if not confirmed
    '''
    for field in fields:
        title = field["Title"]
        value = field["Value"]
        print(f"{title}: {value}")

    new_line()
    response = typer.confirm("Please confirm")
    clear()
    return response