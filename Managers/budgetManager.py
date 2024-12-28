'''
File: budgetManager.py
Project: Managers
File Created: Saturday, 28th December 2024 9:05:33 am
Author: Cortez L. McCrary (cortez.mccrary.codes@gmail.com)
-----
Last Modified: Saturday, 28th December 2024 9:05:49 am
Modified By: Cortez L. McCrary (cortez.mccrary.codes@gmail.com>)
-----
Copyright 2024 Cortez McCrary, Employee of JHU APL
'''
from typing import List
from model import Budget, Project


def get_wbs_list(project: Project):
    '''
    Takes a project object and returns the budget codes associated with the project in a string list
    '''
    wbs_list: List[str] = []
    budgets: List[Budget] = project.budgets
    for budget in budgets:
        wbs_list.append(budget.budget_code)

    return wbs_list