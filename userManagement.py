'''
File: userManagement.py
Project: WorkCalc
File Created: Sunday, 24th November 2024 12:41:51 am
Author: Cortez L. McCrary (cortez.mccrary.codes@gmail.com)
-----
Last Modified: Sunday, 24th November 2024 12:43:04 am
Modified By: Cortez L. McCrary (cortez.mccrary.codes@gmail.com>)
-----
Copyright 2024 Cortez McCrary, Employee of JHU APL
'''


from os import name, system
import sqlite3
from email_validator import validate_email, EmailNotValidError
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from dbController import createUser


clear = lambda: system('cls' if name=='nt' else 'clear')

class ConfirmPasswordError(Exception):
    '''
    Custom Error for when a password does not match it's confirmed value
    '''
    pass

def registerUser(firstName: str, lastName: str, email: str, username: str, password: str, confirmPassword: str, session: Session):
    '''
    Prompts creating a new user 
    '''
    try:
        normalizedEmail = validate_email(email).email
    except EmailNotValidError as e:
            raise e
    
    if password != confirmPassword:
        raise ConfirmPasswordError("Password did not match confirm value.")

    try:
        createUser(firstName=firstName,
                    lastName=lastName,
                    email=email,
                    username=username,
                    password=password,
                    session=session)
    except IntegrityError as e:
         raise e
    except Exception as e:
         raise e

