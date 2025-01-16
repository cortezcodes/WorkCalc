

from datetime import datetime, date, timedelta
import time
from rich import print
from typing import List
import typer
from Managers.budgetManager import get_wbs_list
from Managers.dailyManager import add_event_handler, delete_event_by_id, finish_active_event_handler, get_active_event_handler, print_daily_budget_totals_table, print_event_table, start_event_handler
from Managers.projectManager import get_project_title_list, get_projects_list
from model import Budget, Event, Project
from utils import create_confirmation, display_menu, get_confirmation, new_line, menu_selector, clear, optional_field_handler

# TODO Create Non-billable events
#TODO Change to Today Function
#TODO Create Yearly Report 
#TODO Create Customize date range report

def daily_menu(user_id: int):
    '''
   Creates the main menu for daily task 
    '''
    clear()  
    date_selected: datetime = datetime.now()
    active_event: Event | None = None
    while True:
        active_event = get_active_event_handler(user_id=user_id, target_date=date_selected)
        print_event_table(user_id=user_id, date=date_selected)
        print_daily_budget_totals_table(user_id=user_id, date=date_selected)
        new_line()
        if active_event:
            print(f"Current Active Event:\n\tProject: {active_event.project}\n\tStart Time: {active_event.start_time}" +
                  f"\n\tEvent Description: {active_event.event_description}\n\tBudget: {active_event.budget_code}")
            new_line()
            display_menu(["Change Date", "Forwad Day","Back Day","Today","Finish Event", "Add Event", "Delete Event", "Back to Main Menu"], "Daily Menu")
            new_line()
            selection = menu_selector("Let's Manage your Projects")
            match selection:
                case 1:
                    date_selected = change_date_prompter()
                case 2:
                    date_selected = date_selected + timedelta(days=1)
                    clear()
                case 3:
                    date_selected = date_selected - timedelta(days=1)
                    clear()
                case 4:
                    date_selected = datetime.now()
                    clear()
                case 5:
                    finish_active_event_handler(user_id=user_id, event_id=active_event.id)
                    active_event = None
                case 6:
                    create_event_prompter(user_id=user_id, cur_date=date_selected)
                case 7:
                    delete_event_prompter(user_id=user_id, cur_date=date_selected)
                case 8:
                    clear()
                    break
        elif not active_event and date_selected.date() == date.today():
            display_menu(["Change Date","Forward Day", "Back Day", "Start Event", "Add Event", "Delete Event", "Add Non-billable Event","Back to Main Menu"], "Daily Menu")
            new_line()
            selection = menu_selector("Let's manage your Projects")
            match selection:
                case 1:
                    date_selected = change_date_prompter()
                case 2:
                    date_selected = date_selected + timedelta(days=1)
                    clear()
                case 3:
                    date_selected = date_selected - timedelta(days=1)
                    clear()
                case 4:
                    start_event_prompter(user_id=user_id)
                case 5:
                    create_event_prompter(user_id=user_id, cur_date=date_selected)
                case 6:
                    delete_event_prompter(user_id=user_id, cur_date=date_selected)
                case 7:
                    create_non_billable_event_prompter(user_id=user_id, cur_date=date_selected)
                case 8:
                    clear()
                    break
        else:
            display_menu(["Change Date","Forward Day","Back Day","Today","Add Event", "Delete Event", "Back to Main Menu"], "Daily Menu")
            new_line()
            selection = menu_selector("Let's manage your Projects")
            match selection:
                case 1:
                    date_selected = change_date_prompter()
                case 2:
                    date_selected = date_selected + timedelta(days=1)
                    clear()
                case 3:
                    date_selected = date_selected - timedelta(days=1)
                    clear()
                case 4:
                    date_selected = datetime.now()
                    clear()
                case 5:
                    create_event_prompter(user_id=user_id, cur_date=date_selected)
                case 6:
                    delete_event_prompter(user_id=user_id, cur_date=date_selected)
                case 7:
                    clear()
                    break

def change_date_prompter():
    '''
    prompts the user to change current date being viewed
    '''
    clear()
    new_date = typer.prompt("Date (MM/DD/YYYY)")
    try:
        clear()
        return datetime.strptime(new_date,"%m/%d/%Y")
    except ValueError as e:
        print(f"ValueError: ensure you are using the correct MM/DD/YYYY Format. {e}")

def start_event_prompter(user_id:int):
    '''
    Start an event time now, with no end time. Program can only have one active event at any given time. 
    '''
    while True:
        clear()
        project, budget = budget_selector(user_id=user_id)
        if project and budget:
            event_description = typer.prompt("Event Description")
            new_line()
            isConfirmed = get_confirmation([create_confirmation("Project", project.title),
                    create_confirmation("Budget", budget.budget_code),
                    create_confirmation("Event", event_description)])
            if isConfirmed:
                start_event_handler(user_id=user_id, project=project.title, budget=budget.budget_code, event_description=event_description)
                break
        else:
            break

def create_event_prompter(user_id: int, cur_date: datetime):
    '''
    Menu for creating a new event
    '''
    while True:
        clear()
        project, budget = budget_selector(user_id=user_id)
        if project and budget:
            event = typer.prompt("Event Description")
            new_line()
            print_event_table(user_id=user_id, date=cur_date)
            new_line()
            start_time = typer.prompt("Start Time (0000  - 2359)")
            end_time = typer.prompt("End Time (0000  - 2359)")
            is_complete: bool = True
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
            clear()
            print("Add event cancelled")
            time.sleep(1)
            clear()
            break
    clear()

def delete_event_prompter(user_id: int, cur_date: datetime):
    '''
    Prompts a user for deleting an event for a given day. 
    '''
    clear()
    events: List[Event] = print_event_table(user_id=user_id, date=cur_date, isNumbered=True)
    while True:
        input = typer.prompt("Select an event by it's # (Cancel with input e)")
        if input == 'e':
            return
        
        input = int(input)-1
        if input >= 0 and input < len(events):
            event: Event = events[input]
            clear()
            delete_event_by_id(user_id=user_id, event_id=event.id)
            new_line()
            return
        else:
            print("Invalid input")

def create_non_billable_event_prompter(user_id: int, cur_date: datetime):
    '''
    Used to create an event that does not get included into your billable hours
    '''
    while True:
        clear()
        event_titles: List[str] = ["Lunch", "Sick time", "Personal Time", "Administrative", "Holiday", "Other", "Back to Event Menu"]
        event_budget_dict: dict[str] = {
            "Lunch":"Lunch", 
            "Sick Time":"Sick",
            "Personal Time": "Personal",
            "Administrative":"Admin",
            "Holiday": "Holiday",
            "Other": "Other"}
        event_selected: str = None
        budget_selected: str = None
        while not budget_selected or not event_selected:
            display_menu(event_titles, "Events")
            new_line()
            selection = int(menu_selector("Select an Event"))
            if selection == len(event_titles):
                return
            elif selection <= len(event_titles) and selection > 0:
                event_selected = event_titles[selection-1]
                budget_selected = event_budget_dict.get(event_selected)
        
        if event_selected and budget_selected:
            print_event_table(user_id=user_id, date=cur_date)
            new_line()
            start_time = typer.prompt("Start Time (0000  - 2359)")
            end_time = typer.prompt("End Time (0000  - 2359)")
            is_complete: bool = True
            clear()

            isConfirmed = get_confirmation([create_confirmation("Event", event_selected),
                                create_confirmation("Start", start_time),
                                create_confirmation("End", end_time),
                                create_confirmation("Complete?", is_complete)])
            if isConfirmed:
                try:
                    add_event_handler(user_id=user_id, date=cur_date, project="", 
                                    budget=budget_selected, event_description=event_selected, start_time=start_time,
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
            clear()
            print("Add event cancelled")
            time.sleep(1)
            clear()
            break
    clear()

def delete_event_prompter(user_id: int, cur_date: datetime):
    '''
    Prompts a user for deleting an event for a given day. 
    '''
    clear()
    events: List[Event] = print_event_table(user_id=user_id, date=cur_date, isNumbered=True)
    while True:
        input = typer.prompt("Select an event by it's # (Cancel with input e)")
        if input == 'e':
            return
        
        input = int(input)-1
        if input >= 0 and input < len(events):
            event: Event = events[input]
            clear()
            delete_event_by_id(user_id=user_id, event_id=event.id)
            new_line()
            return
        else:
            print("Invalid input")




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