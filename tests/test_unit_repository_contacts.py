from datetime import date
import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactModel
from src.repository.contacts import (
    get_contacts,
    get_contact_by_id,
    get_contact_by_email,
    create_contact,
    update,
    remove,
    get_contact_by_first_name,
    get_contact_by_last_name,
)


class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_get_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter_by().limit().offset().all.return_value = contacts
        result = await get_contacts(limit=10, offset=0, user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contact_by_id_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await get_contact_by_id(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_get_contact_by_id_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_contact_by_id(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_get_contact_by_email_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await get_contact_by_email(contact_email='fake@fake.com', user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_get_contact_by_email_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_contact_by_email(contact_email='fake@fake.com', user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_create_contact(self):
        body = ContactModel(first_name='Alex', last_name='King', email='fake@fake.com', phone='+380990000000',
                            birthday=date(1994, 5, 2))
        result = await create_contact(body=body, user=self.user, db=self.session)
        self.assertEqual(result.first_name, body.first_name)
        self.assertEqual(result.last_name, body.last_name)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone, body.phone)
        self.assertEqual(result.birthday, body.birthday)

    async def test_update_found(self):
        body = ContactModel(first_name='Alex', last_name='King', email='fake@fake.com', phone='+380990000000',
                            birthday=date(1994, 5, 2))
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        self.session.commit.return_value = None
        result = await update(contact_id=1, body=body, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_update_not_found(self):
        body = ContactModel(first_name='Alex', last_name='King', email='fake@fake.com', phone='+380990000000',
                            birthday=date(1994, 5, 2))
        self.session.query().filter().first.return_value = None
        self.session.commit.return_value = None
        result = await update(contact_id=1, body=body, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_remove_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await remove(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_remove_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await remove(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_get_contact_by_first_name_found(self):
        contact = Contact()
        self.session.query().filter().all.return_value = contact
        result = await get_contact_by_first_name(contact_first_name='Alex', user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_get_contact_by_first_name_not_found(self):
        self.session.query().filter().all.return_value = None
        result = await get_contact_by_first_name(contact_first_name='Alex', user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_get_contact_by_last_name_found(self):
        contact = Contact()
        self.session.query().filter().all.return_value = contact
        result = await get_contact_by_last_name(contact_last_name='King', user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_get_contact_by_last_name_not_found(self):
        self.session.query().filter().all.return_value = None
        result = await get_contact_by_last_name(contact_last_name='King', user=self.user, db=self.session)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
