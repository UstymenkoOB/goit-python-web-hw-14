from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.schemas import ContactModel, ContactUpdate, ContactResponse
from src.repository import contacts as repository_contacts
from src.routes.auth import auth_service


router = APIRouter(prefix='/contacts', tags=["contacts"])


@router.get("/", response_model=List[ContactResponse], description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def read_contacts(skip: int = 0, limit: int = 100,
                        current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    """
    Retrieve a list of contacts for the current user.

    :param skip: Number of contacts to skip.
    :type skip: int
    :param limit: Maximum number of contacts to return.
    :type limit: int
    :param current_user: The authenticated user.
    :type current_user: User
    :param db: Database session.
    :type db: Session
    :return: List of contacts for the current user.
    :rtype: List[ContactResponse]
    """
    contacts = await repository_contacts.get_contacts(skip, limit, current_user, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse, description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def read_contact(contact_id: int, db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    """
    Retrieve a single contact by ID for the current user.

    :param contact_id: The ID of the contact to retrieve.
    :type contact_id: int
    :param db: Database session.
    :type db: Session
    :param current_user: The authenticated user.
    :type current_user: User
    :return: The contact with the specified ID.
    :rtype: ContactResponse
    """
    contact = await repository_contacts.get_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.get("/search/name", response_model=List[ContactResponse], description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def read_contacts_name(name: str, db: Session = Depends(get_db),
                             current_user: User = Depends(auth_service.get_current_user)):
    """
    Search for contacts by name for the current user.

    :param name: The name to search for in contacts.
    :type name: str
    :param db: Database session.
    :type db: Session
    :param current_user: The authenticated user.
    :type current_user: User
    :return: List of contacts matching the search criteria.
    :rtype: List[ContactResponse]
    """
    contacts = await repository_contacts.get_contacts_name(name, current_user, db)
    if not contacts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contacts


@router.get("/search/surname", response_model=List[ContactResponse], description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def read_contacts_surname(surname: str, db: Session = Depends(get_db),
                                current_user: User = Depends(auth_service.get_current_user)):
    """
    Search for contacts by surname for the current user.

    :param surname: The surname to search for in contacts.
    :type surname: str
    :param db: Database session.
    :type db: Session
    :param current_user: The authenticated user.
    :type current_user: User
    :return: List of contacts matching the search criteria.
    :rtype: List[ContactResponse]
    """
    contacts = await repository_contacts.get_contacts_surname(surname, current_user, db)
    if not contacts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contacts


@router.get("/search/email", response_model=List[ContactResponse], description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def read_contacts_email(email: str, db: Session = Depends(get_db),
                              current_user: User = Depends(auth_service.get_current_user)):
    """
    Search for contacts by email for the current user.

    :param email: The email to search for in contacts.
    :type email: str
    :param db: Database session.
    :type db: Session
    :param current_user: The authenticated user.
    :type current_user: User
    :return: List of contacts matching the search criteria.
    :rtype: List[ContactResponse]
    """
    contacts = await repository_contacts.get_contacts_email(email, current_user, db)
    if not contacts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contacts


@router.get("/search/birthdays", response_model=List[ContactResponse], description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def read_birthdays(db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    Retrieve contacts with upcoming birthdays for the current user.

    :param db: Database session.
    :type db: Session
    :param current_user: The authenticated user.
    :type current_user: User
    :return: List of contacts with upcoming birthdays.
    :rtype: List[ContactResponse]
    """
    contacts = await repository_contacts.get_contacts_birthday(current_user, db)
    if not contacts:  
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contacts not found")
    return contacts


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED, description='No more than 10 requests per minute',
             dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def create_contact(body: ContactModel, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    Create a new contact for the current user.

    :param body: Data for creating a new contact.
    :type body: ContactModel
    :param db: Database session.
    :type db: Session
    :param current_user: The authenticated user.
    :type current_user: User
    :return: The newly created contact.
    :rtype: ContactResponse
    """
    return await repository_contacts.create_contact(body, current_user, db)


@router.put("/{contact_id}", response_model=ContactResponse, description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def update_contact(body: ContactUpdate, contact_id: int, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    Update an existing contact for the current user.

    :param body: Data for updating the contact.
    :type body: ContactUpdate
    :param contact_id: The ID of the contact to update.
    :type contact_id: int
    :param db: Database session.
    :type db: Session
    :param current_user: The authenticated user.
    :type current_user: User
    :return: The updated contact.
    :rtype: ContactResponse
    """
    contact = await repository_contacts.update_contact(contact_id, body, current_user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse, description='No more than 10 requests per minute',
               dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def remove_contact(contact_id: int, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    Remove a contact for the current user.

    :param contact_id: The ID of the contact to remove.
    :type contact_id: int
    :param db: Database session.
    :type db: Session
    :param current_user: The authenticated user.
    :type current_user: User
    :return: The removed contact.
    :rtype: ContactResponse
    """
    contact = await repository_contacts.remove_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact
