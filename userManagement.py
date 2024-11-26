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
from dbController import create_user, login


clear = lambda: system('cls' if name=='nt' else 'clear')

class ConfirmPasswordError(Exception):
    '''
    Custom Error for when a password does not match it's confirmed value
    '''
    pass
class EmptyFieldError(Exception):
    '''
    Exception thrown when a required field is empty
    '''
    pass

class WrongCredentialsError(Exception):
    '''
    Exception thrown when a wrong password is entered
    '''
    pass

def register_user_handler(firstName: str, lastName: str, email: str, username: str, password: str, confirmPassword: str, session: Session):
    '''
    Prompts creating a new user 
    '''
    try:
        normalizedEmail = validate_email(email).email
    except Exception as e:
            raise e
    
    if password != confirmPassword:
        raise ConfirmPasswordError("Password did not match confirm value.")

    try:
        create_user(firstName=firstName,
                    lastName=lastName,
                    email=email,
                    username=username,
                    password=password,
                    session=session)
    except Exception as e:
         raise e

def login_handler(username: str, password:str, session: Session):
    '''
    Strips spaces from leading and trailing characters of username and password before querying to login a user
    '''
    username = username.strip()
    password = password.strip()
    if not username or not password:
        raise EmptyFieldError("EmptyFieldError: Required field left blank.")
    try: 
        user = login(username=username, password=password, session=session)
        if user:
            return user
        else:
            raise WrongCredentialsError("Incorrect username and/or password")
    except Exception as e:
        raise e