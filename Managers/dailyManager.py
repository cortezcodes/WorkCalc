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
from dbController import add_event


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