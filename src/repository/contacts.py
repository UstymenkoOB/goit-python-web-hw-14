from datetime import date, timedelta
from typing import List
from sqlalchemy import String, and_, extract, func, or_
from sqlalchemy.orm import Session
from src.database.models import Contact, User
from src.schemas import ContactModel, ContactUpdate

async def get_contacts(skip: int, limit: int, user: User, db: Session) -> List[Contact]:
    """
    Retrieves a list of contacts for a specific user with specified pagination parameters.

    :param skip: The number of contacts to skip.
    :type skip: int
    :param limit: The maximum number of contacts to return.
    :type limit: int
    :param user: The user to retrieve contacts for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: A list of contacts.
    :rtype: List[Contact]
    """
    return db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()

async def get_contact(contact_id: int, user: User, db: Session) -> Contact:
    """
    Retrieves a single contact with the specified ID for a specific user.

    :param contact_id: The ID of the contact to retrieve.
    :type contact_id: int
    :param user: The user to retrieve the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The contact with the specified ID, or None if it does not exist.
    :rtype: Contact | None
    """
    return db.query(Contact).filter(and_(Contact.id == contact_id), Contact.user_id == user.id).first()

async def get_contacts_name(name: str, user: User, db: Session) -> List[Contact]:
    """
    Retrieves a list of contacts for a specific user with a name that contains the specified substring.

    :param name: The substring to search for in the contact names.
    :type name: str
    :param user: The user to retrieve contacts for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: A list of contacts that match the search criteria.
    :rtype: List[Contact]
    """
    return db.query(Contact).filter(and_(Contact.name.like(f'%{name}%'), Contact.user_id == user.id)).all()

async def get_contacts_surname(surname: str, user: User, db: Session) -> List[Contact]:
    """
    Retrieves a list of contacts for a specific user with a surname that contains the specified substring.

    :param surname: The substring to search for in the contact surnames.
    :type surname: str
    :param user: The user to retrieve contacts for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: A list of contacts that match the search criteria.
    :rtype: List[Contact]
    """
    return db.query(Contact).filter(and_(Contact.surname.like(f'%{surname}%'), Contact.user_id == user.id)).all()

async def get_contacts_email(email_part: str, user: User, db: Session) -> List[Contact]:
    """
    Retrieves a list of contacts for a specific user with an email that contains the specified substring.

    :param email_part: The substring to search for in the contact emails.
    :type email_part: str
    :param user: The user to retrieve contacts for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: A list of contacts that match the search criteria.
    :rtype: List[Contact]
    """
    return db.query(Contact).filter(and_(Contact.email.like(f'%{email_part}%'), Contact.user_id == user.id)).all()

async def get_contacts_birthday(user: User, db: Session) -> List[Contact]:
    """
    Retrieves a list of contacts for a specific user with birthdays in the next 7 days.

    :param user: The user to retrieve contacts for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: A list of contacts with birthdays in the next 7 days.
    :rtype: List[Contact]
    """
    days = []
    for i in range(7):
        day = date.today() + timedelta(days=i)
        days.append(str(day.day) + str(day.month))
    contacts = db.query(Contact).filter(and_(
        or_(func.concat(
        extract('day', Contact.birthday).cast(String),
        extract('month', Contact.birthday).cast(String)
        ).in_(days))), Contact.user_id == user.id).all()
    return contacts

async def create_contact(body: ContactModel, user: User, db: Session) -> Contact:
    """
    Creates a new contact for a specific user.

    :param body: The data for the contact to create.
    :type body: ContactModel
    :param user: The user to create the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The newly created contact.
    :rtype: Contact
    """
    contact = Contact(name=body.name, surname=body.surname, email=body.email, 
                      phone=body.phone, birthday=body.birthday, 
                      description=body.description, user_id=user.id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact

async def remove_contact(contact_id: int, user: User, db: Session) -> Contact | None:
    """
    Removes a single contact with the specified ID for a specific user.

    :param contact_id: The ID of the contact to remove.
    :type contact_id: int
    :param user: The user to remove the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The removed contact, or None if it does not exist.
    :rtype: Contact | None
    """
    contact = db.query(Contact).filter(
        and_(Contact.id == contact_id), Contact.user_id == user.id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact

async def update_contact(contact_id: int, body: ContactUpdate, user: User, db: Session) -> Contact | None:
    """
    Updates a single contact with the specified ID for a specific user.

    :param contact_id: The ID of the contact to update.
    :type contact_id: int
    :param body: The updated data for the contact.
    :type body: ContactUpdate
    :param user: The user to update the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The updated contact, or None if it does not exist.
    :rtype: Contact | None
    """
    contact = db.query(Contact).filter(
        and_(Contact.id == contact_id), Contact.user_id == user.id).first()
    if contact:
        contact.name = body.name
        contact.surname = body.surname
        contact.email = body.email
        contact.phone = body.phone
        contact.birthday = body.birthday
        contact.description = body.description
        db.commit()
    return contact
