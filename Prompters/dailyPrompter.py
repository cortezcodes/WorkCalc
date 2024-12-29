

from datetime import datetime
import time
from typing import List
import typer
from Managers.budgetManager import get_wbs_list
from Managers.dailyManager import add_event_handler, print_daily_budget_totals_table, print_event_table
from Managers.projectManager import get_project_title_list, get_projects_list
from model import Budget, Project
from utils import create_confirmation, display_menu, get_confirmation, new_line, menu_selector, clear, optional_field_handler

date_selected: datetime = datetime.now()

def daily_menu(user_id: int):
    '''
   Creates the main menu for daily task 
    '''
    clear()
    while True:
        print_event_table(user_id=user_id, date=date_selected)
        new_line()
        print_daily_budget_totals_table(user_id=user_id, date=date_selected)
        new_line()
        display_menu(["Change Date","Start Event", "Finish Event", "Add Event", "Delete Event", "Back to Main Menu"], "Daily Menu")
        new_line()
        selection = menu_selector("Let's manage your Projects")
        match selection:
            case 1:
                print("Change Date")
            case 2:
                print("start event")
            case 3:
                print("finish event")
            case 4:
                create_event_prompter(user_id=user_id, cur_date=date_selected)
            case 5:
                print("Delete Event")
            case 6:
                clear()
                break

def create_event_prompter(user_id: int, cur_date: datetime):
    '''
    Menu for creating a new event
    '''
    clear()
    while True:

        project, budget = budget_selector(user_id=user_id)
        if project and budget:
            event = typer.prompt("Event Description")
            start_time = typer.prompt("Start Time (0000  - 2359)")
            end_time = optional_field_handler(typer.prompt("End Time (0000  - 2359)", default="optional"))
            is_complete: bool = None
            if end_time:
                is_complete = True
            else:
                is_complete = False
            clear()

            isConfirmed = get_confirmation([create_confirmation("Project", project.title),
                                create_confirmation("Budget", budget.budget_code),
                                create_confirmation("Event", event),
                                create_confirmation("Start", start_time),
                                create_confirmation("End", end_time),
                                create_confirmation("Complete?", is_complete)])
            if isConfirmed:
                try:
                    add_event_handler(user_id=user_id, date=cur_date, project=project.title, 
                                    budget=budget.budget_code, event_description=event, start_time=start_time,
                                    end_time=end_time, isComplete=is_complete)
                except ValueError as e:
                    print(f"ValueError: {e}")
                    new_line()
                    return
                
                print("Event created")
                time.sleep(1)
                clear()
                break
        else:
            break
    clear()

def budget_selector(user_id: int):
    '''
    Menu for selecting a budget to log with an event. Retuns a str of the project and the budget 
    '''
    project_titles: List[str] = get_project_title_list(user_id=user_id)
    project_titles.append("Back to Event Menu")
    projects: List[Project] = get_projects_list(user_id=user_id)
    project_selected: Project = None
    budget_selected: str = None
    while not project_selected:
        display_menu(project_titles, "Projects")
        new_line()
        selection = int(menu_selector("Select a project"))
        if selection == len(project_titles):
            return None, None
        elif selection <= len(project_titles) and selection > 0:
            project_selected = projects[selection-1]

    while not budget_selected:
        # TODO Create a way to retrieve a list of the budget WBS. 
        budget_list: List[str] = get_wbs_list(project_selected)
        budget_list.append("Back to Event Menu")
        display_menu(budget_list, "Budgets")
        new_line()
        selection = int(menu_selector("Select a Budget"))
        if selection == len(budget_list):
            return None, None
        elif selection <= len(project_selected.budgets) and selection > 0:
            budget_selected = project_selected.budgets[selection-1]

    return project_selected, budget_selected

def delete_event_prompter(user_id: int):
    '''
    Menu for deleting an event
    '''