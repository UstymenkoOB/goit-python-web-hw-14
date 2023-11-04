import unittest

from datetime import date, timedelta

from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactModel, ContactUpdate
from src.repository.contacts import (
    get_contacts,
    get_contact,
    get_contacts_name,
    get_contacts_surname,
    get_contacts_email,
    get_contacts_birthday,
    create_contact,
    remove_contact,
    update_contact,
)


class TestContactFunctions(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_get_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().offset().limit().all.return_value = contacts
        result = await get_contacts(skip=0, limit=10, user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contact(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_get_contact_nonexistent(self):
        self.session.query().filter().first.return_value = None
        result = await get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_get_contacts_name(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().all.return_value = contacts
        result = await get_contacts_name("John", user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contacts_surname(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().all.return_value = contacts
        result = await get_contacts_surname("Doe", user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contacts_email(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().all.return_value = contacts
        result = await get_contacts_email("example.com", user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contacts_birthday(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().all.return_value = contacts
        result = await get_contacts_birthday(user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_create_contact(self):
        contact_data = ContactModel(
            name="John",
            surname="Doe",
            email="john@example.com",
            phone="1234567890",
            birthday=date.today(),
            description="A test contact",
        )
        contact = Contact(**contact_data.dict(), user_id=self.user.id)
        self.session.add(contact)
        self.session.commit.return_value = None
        self.session.refresh(contact)
        result = await create_contact(body=contact_data, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_remove_contact_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        self.session.delete(contact)
        self.session.commit.return_value = None
        result = await remove_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_remove_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await remove_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_update_contact_found(self):
        contact_data = ContactUpdate(
            name="Updated John",
            surname="Updated Doe",
            email="updated@example.com",
            phone="9876543210",
            birthday=date.today() - timedelta(days=365),
            description="Updated contact",
        )
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        contact.name = contact_data.name
        contact.surname = contact_data.surname
        contact.email = contact_data.email
        contact.phone = contact_data.phone
        contact.birthday = contact_data.birthday
        contact.description = contact_data.description
        self.session.commit.return_value = None
        result = await update_contact(contact_id=1, body=contact_data, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_update_contact_not_found(self):
        contact_data = ContactUpdate(
            name="Updated John",
            surname="Updated Doe",
            email="updated@example.com",
            phone="9876543210",
            birthday=date.today() - timedelta(days=365),
            description="Updated contact",
        )
        self.session.query().filter().first.return_value = None
        result = await update_contact(contact_id=1, body=contact_data, user=self.user, db=self.session)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
