from datetime import date, timedelta

from sqlalchemy import extract, and_
from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactModel


async def get_contacts(limit: int, offset: int, user: User, db: Session):
    """
    The get_contacts function returns a list of contacts for the user.

    :param limit: int: Limit the number of contacts returned
    :param offset: int: Specify the number of records to skip before starting to return rows
    :param user: User: Get the user id from the database
    :param db: Session: Pass the database session to the function
    :return: A list of contacts
    :doc-author: Trelent
    """
    contacts = db.query(Contact).filter_by(user_id=user.id).limit(limit).offset(offset).all()
    return contacts


async def get_contact_by_id(contact_id: int, user: User, db: Session):
    """
    The get_contact_by_id function returns a contact object from the database based on the user's id and
    the contact's id. The function takes in three parameters:
        -contact_id: an integer representing the unique identifier of a specific contact.
        -user: an object representing a user that is logged into our application. This parameter is used to ensure that
        only contacts belonging to this particular user are returned by this function.
        -db: an SQLAlchemy Session instance, which represents our connection to the database.

    :param contact_id: int: Specify the id of the contact to be retrieved
    :param user: User: Get the user_id from the user object
    :param db: Session: Pass the database session to the function
    :return: A contact object
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter(and_(Contact.user_id == user.id, Contact.id == contact_id)).first()
    return contact


async def get_contact_by_email(contact_email: str, user: User, db: Session):
    """
    The get_contact_by_email function takes in a contact_email and user object, and returns the contact with that email.
        Args:
            contact_email (str): The email of the desired Contact.
            user (User): The User who owns the desired Contact.

    :param contact_email: str: Specify the email of the contact to be retrieved
    :param user: User: Get the user_id from the database
    :param db: Session: Access the database
    :return: The contact with the given email address, if it exists
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter(and_(Contact.user_id == user.id, Contact.email == contact_email)).first()
    return contact


async def create_contact(body: ContactModel, user: User, db: Session):
    """
    The create_contact function creates a new contact in the database.

    :param body: ContactModel: Create a new contact object
    :param user: User: Get the user id from the token
    :param db: Session: Pass the database session to the function
    :return: The contact that was created
    :doc-author: Trelent
    """
    contact = Contact(**body.dict(), user=user)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update(contact_id: int, body: ContactModel, user: User, db: Session):
    """
    The update function updates a contact in the database.
        Args:
            contact_id (int): The id of the contact to update.
            body (ContactModel): The updated information for the specified user.

    :param contact_id: int: Get the contact by id
    :param body: ContactModel: Get the data from the request body
    :param user: User: Get the user_id from the token
    :param db: Session: Access the database
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await get_contact_by_id(contact_id, user, db)
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone = body.phone
        contact.birthday = body.birthday
        db.commit()
    return contact


async def remove(contact_id: int, user: User, db: Session):
    """
    The remove function removes a contact from the database.
        Args:
            contact_id (int): The id of the contact to be removed.
            user (User): The user who is removing the contact.
            db (Session): A connection to our database, used for querying and updating data.

    :param contact_id: int: Get the contact by id
    :param user: User: Check if the contact belongs to the user
    :param db: Session: Pass the database session to the function
    :return: The contact that was removed
    :doc-author: Trelent
    """
    contact = await get_contact_by_id(contact_id, user, db)
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def get_contact_by_first_name(contact_first_name: str, user: User, db: Session):
    """
    The get_contact_by_first_name function takes in a contact first name, user, and db as parameters.
    It then queries the database for all contacts that match the given first name and returns them.

    :param contact_first_name: str: Filter the contacts by first name
    :param user: User: Get the user id from the database
    :param db: Session: Pass in the database session
    :return: A list of contacts that match the first name provided
    :doc-author: Trelent
    """
    contacts = db.query(Contact).filter(
        and_(Contact.user_id == user.id, Contact.first_name == contact_first_name)).all()
    return contacts


async def get_contact_by_last_name(contact_last_name: str, user: User, db: Session):
    """
    The get_contact_by_last_name function returns a list of contacts with the given last name.
        Args:
            contact_last_name (str): The last name of the contact to be retrieved.
            user (User): The user who is making this request. This is used for authorization purposes, as only users can access their own contacts.
            db (Session): A database session object that will be used to query the database and retrieve all matching contacts.

    :param contact_last_name: str: Filter the contacts by last name
    :param user: User: Get the user id from the user object
    :param db: Session: Connect to the database
    :return: A list of contacts with the last name specified in the function call
    :doc-author: Trelent
    """
    contacts = db.query(Contact).filter(
        and_(Contact.user_id == user.id, Contact.last_name == contact_last_name)).all()
    return contacts


async def get_birthday(user: User, db: Session):
    """
    The get_birthday function returns a list of contacts whose birthday is within the next week.
        Args:
            user (User): The user who's contacts are being searched for birthdays.
            db (Session): A database session object to query the database with.

    :param user: User: Get the user id from the database
    :param db: Session: Pass the database session to the function
    :return: A list of contacts whose birthday is within the next 7 days
    :doc-author: Trelent
    """
    today = date.today()
    next_week = today + timedelta(days=7)
    contacts = db.query(Contact).filter(and_(Contact.user_id == user.id, extract('day', Contact.birthday) >= today.day,
                                             extract('day', Contact.birthday) <= next_week.day,
                                             extract('month', Contact.birthday) == today.month)).all()
    return contacts
