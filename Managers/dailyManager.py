'''
File: dailyManager.py
Project: Managers
File Created: Wednesday, 25th December 2024 4:35:46 pm
Author: Cortez L. McCrary (cortez.mccrary.codes@gmail.com)
-----
Last Modified: Saturday, 28th December 2024 10:06:38 am
Modified By: Cortez L. McCrary (cortez.mccrary.codes@gmail.com>)
-----
Copyright 2024 Cortez McCrary, Employee of JHU APL
'''
from datetime import datetime
from typing import List
from dbController import add_event, get_events_on_date
from model import Event
from utils import create_table, get_total_hours


def add_event_handler(user_id: int, date: datetime, project: str, budget: str, 
              event_description: str, start_time: str, end_time: str | None, isComplete: bool ):
    '''
    Handles preprocessing parameters for creating a event database entry
    '''
    # validate times
    start = int(start_time)
    if start < 0 or start >= 2400:
        raise ValueError("Start time invalid time")
    if end_time:
        end = int(end_time)
    if end < 0 or end >= 2400:
        raise ValueError("End time invalid time")
    
    start_hour = int(start_time[:2])
    start_minutes = int(start_time[2:])
    start_datetime = date.replace(hour=start_hour, minute=start_minutes, second=0, microsecond=0)
    if end_time:
        end_hour = int(end_time[:2])
        end_minute = int(end_time[2:])
        end_datetime = date.replace(hour=end_hour, minute=end_minute, second=0, microsecond=0)
    
    add_event(user_id=user_id, project=project, budget=budget, 
              event_description=event_description, start_time=start_datetime,
              end_time=end_datetime, isComplete=isComplete)
    
def print_event_table(user_id:int, date: datetime):
    '''
    Prints current dates event table
    '''
    headers=["Start", "End", "Total Time", "Project", "Event Description", "Budget"]
    events: List[Event] = get_events_on_date(user_id, date)
    rows: List[list] = []
    for event in events:
        total_hours = get_total_hours(event.start_time, event.end_time)
        rows.append([event.start_time.strftime("%H:%M"), event.end_time.strftime("%H:%M"),
                     str(total_hours), event.project, event.event_description, event.budget_code])
    formatted_date = date.strftime("%m/%d/%Y")
    create_table(title=f"Events on {formatted_date}", headers=headers, rows=rows)

def print_daily_budget_totals_table(user_id: int, date: datetime):
    '''
    Prints table for displaying totals for a given day based on budgets
    '''
    headers=["Budget", "hours"]
    events: List[Event] = get_events_on_date(user_id, date)
    rows:List[list] = []
    budget_totals: dict = {}
    daily_total_hours = 0
    for event in events:
        total_hours = get_total_hours(event.start_time, event.end_time)
        daily_total_hours = daily_total_hours + total_hours
        if event.budget_code not in budget_totals.keys():
            budget_totals[event.budget_code] = total_hours
        else:
            budget_totals[event.budget_code] = budget_totals[event.budget_code] + total_hours

    for budget, value in budget_totals.items():
        rows.append([budget, str(value)])
    
    rows.append(["Total", str(round(daily_total_hours, 2))])
    create_table(title="Daily Budget Totals", headers=headers, rows=rows)