from typing import List

from fastapi import Depends, HTTPException, Path, status, APIRouter, Query
from sqlalchemy.orm import Session
from fastapi_limiter.depends import RateLimiter

from src.database.db import get_db
from src.database.models import User
from src.repository import contacts as repository_contacts
from src.schemas import ContactResponse, ContactModel
from src.services.auth import auth_service

router = APIRouter(prefix='/contacts', tags=['contacts'])


@router.get('/', response_model=List[ContactResponse], dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def get_contacts(limit: int = Query(10, le=100), offset: int = 0,
                       current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    """
    The get_contacts function returns a list of contacts.

    :param limit: int: Limit the number of contacts returned
    :param le: Limit the number of contacts returned
    :param offset: int: Skip the first offset contacts
    :param current_user: User: Get the current user from the database
    :param db: Session: Pass the database session to the repository layer
    :return: A list of contact objects
    :doc-author: Trelent
    """
    contacts = await repository_contacts.get_contacts(limit, offset, current_user, db)
    return contacts


@router.post('/', response_model=ContactResponse, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def create_contact(body: ContactModel, current_user: User = Depends(auth_service.get_current_user),
                         db: Session = Depends(get_db)):
    """
    The create_contact function creates a new contact in the database.
        It takes an email, first_name and last_name as parameters.
        The function returns the newly created contact object.

    :param body: ContactModel: Get the data from the request body
    :param current_user: User: Get the user id from the token
    :param db: Session: Get the database session
    :return: The created contact
    :doc-author: Trelent
    """
    contact = await repository_contacts.get_contact_by_email(body.email, current_user, db)
    if contact:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Email is exists')
    contact = await repository_contacts.create_contact(body, current_user, db)
    return contact


@router.get('/birthday', response_model=List[ContactResponse], dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def search_contact_7_days_birthday(current_user: User = Depends(auth_service.get_current_user),
                                         db: Session = Depends(get_db)):
    """
    The search_contact_7_days_birthday function searches for contacts that have a birthday in the next 7 days.
        It returns a list of contacts with their name, email and date of birth.

    :param current_user: User: Get the current user
    :param db: Session: Access the database
    :return: A list of contacts whose birthday is in the next 7 days
    :doc-author: Trelent
    """
    contacts = await repository_contacts.get_birthday(current_user, db)
    if len(contacts) < 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not Found')
    return contacts


@router.get('/{contact_id}', response_model=ContactResponse, dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def get_contact(contact_id: int = Path(ge=1), current_user: User = Depends(auth_service.get_current_user),
                      db: Session = Depends(get_db)):
    """
    The get_contact function is a GET request that returns the contact with the specified ID.
    The function takes in an integer as a path parameter, and uses it to query for the contact.
    If no such contact exists, then an HTTP 404 error is returned.

    :param contact_id: int: Get the contact id from the path
    :param current_user: User: Get the current user from the database
    :param db: Session: Pass the database session to the repository layer
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await repository_contacts.get_contact_by_id(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not Found')
    return contact


@router.put('/{contact_id}', response_model=ContactResponse, dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def update_contact(body: ContactModel, contact_id: int = Path(ge=1),
                         current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    """
    The update_contact function updates a contact in the database.
        The function takes an id, body and current_user as parameters.
        It then calls the update method of repository_contacts to update a contact in the database.


    :param body: ContactModel: Get the data from the request body
    :param contact_id: int: Specify the path parameter that will be used to identify the contact
    :param current_user: User: Get the current user
    :param db: Session: Get the database session
    :return: The updated contact
    :doc-author: Trelent
    """
    contact = await repository_contacts.update(contact_id, body, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not Found')
    return contact


@router.delete('/{contact_id}', status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def remove_contact(contact_id: int = Path(ge=1), current_user: User = Depends(auth_service.get_current_user),
                         db: Session = Depends(get_db)):
    """
    The remove_contact function removes a contact from the database.

    :param contact_id: int: Get the contact id from the url path
    :param current_user: User: Access the current user's information
    :param db: Session: Pass the database session to the repository layer
    :return: A contact object, which is the same as what we get from the create_contact function
    :doc-author: Trelent
    """
    contact = await repository_contacts.remove(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not Found')
    return contact


@router.get('/search/{contact_email}', response_model=ContactResponse,
            dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def search_contact_by_email(contact_email: str, current_user: User = Depends(auth_service.get_current_user),
                                  db: Session = Depends(get_db)):
    """
    The search_contact_by_email function searches for a contact by email.
        Returns:
            A single Contact object, if found. Otherwise, raises an HTTPException with status code 404 Not Found.

    :param contact_email: str: Pass the contact email to search for
    :param current_user: User: Get the current user from the auth_service
    :param db: Session: Pass the database session to the repository layer
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await repository_contacts.get_contact_by_email(contact_email, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not Found')
    return contact


@router.get('/search/first_name/{contact_first_name}', response_model=List[ContactResponse],
            dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def search_contact_by_first_name(contact_first_name: str,
                                       current_user: User = Depends(auth_service.get_current_user),
                                       db: Session = Depends(get_db)):
    """
    The search_contact_by_first_name function searches for a contact by first name.
        Args:
            contact_first_name (str): The first name of the contact to search for.
            current_user (User): The user who is making the request. This is passed in automatically by FastAPI's Depends() function, which uses auth_service to get the current user from their JWT token in their HTTP Authorization header.
            db (Session): A database session object that allows us to make queries against our database using SQLAlchemy's ORM syntax and methods, such as .query(). This is passed in automatically by Fast

    :param contact_first_name: str: Pass in the first name of the contact to search for
    :param current_user: User: Get the current user from the database
    :param db: Session: Pass the database session to the repository layer
    :return: A list of contacts that match the first name
    :doc-author: Trelent
    """
    contacts = await repository_contacts.get_contact_by_first_name(contact_first_name, current_user, db)
    if len(contacts) < 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not Found')
    return contacts


@router.get('/search/last_name/{contact_last_name}', response_model=List[ContactResponse],
            dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def search_contact_by_last_name(contact_last_name: str,
                                       current_user: User = Depends(auth_service.get_current_user),
                                       db: Session = Depends(get_db)):
    """
    The search_contact_by_last_name function searches for a contact by last name.
        Args:
            contact_last_name (str): The last name of the contact to search for.
            current_user (User): The user who is making the request. This is passed in via dependency injection, and will be
            automatically populated when you use this function from an endpoint that has been decorated with @router.get().

    :param contact_last_name: str: Search the database for a contact with that last name
    :param current_user: User: Get the current user from the auth_service
    :param db: Session: Get the database session
    :return: A list of contacts with the same last name
    :doc-author: Trelent
    """
    contacts = await repository_contacts.get_contact_by_last_name(contact_last_name, current_user, db)
    if len(contacts) < 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not Found')
    return contacts
