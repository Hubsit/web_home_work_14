import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel
from src.repository.users import (
    get_user_by_email,
    create_user,
    update_token,
    confirmed_email,
    update_avatar
)


class TestUsers(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)

    async def test_get_user_by_email_found(self):
        user = User()
        self.session.query().filter_by().first.return_value = user
        result = await get_user_by_email(email='test@test.com', db=self.session)
        self.assertEqual(result, user)

    async def test_get_contact_by_id_not_found(self):
        self.session.query().filter_by().first.return_value = None
        result = await get_user_by_email(email='test@test.com', db=self.session)
        self.assertIsNone(result)

    async def test_create_user(self):
        body = UserModel(username='Test', email='test@test.com', password='testqwerty')
        result = await create_user(body=body, db=self.session)
        self.assertEqual(result.username, body.username)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.password, body.password)

    async def test_update_token(self):
        user = User()
        user.refresh_token = None
        refresh_token = 'test_token'
        await update_token(user=user, refresh_token=refresh_token, db=self.session)
        self.assertEqual(user.refresh_token, refresh_token)

    async def test_confirmed_email(self):
        user = User(email='test@test.com', confirmed=False)
        self.session.add(user)
        self.session.commit()
        user_id = user.id
        await confirmed_email(email=user.email, db=self.session)
        confirmed_user = self.session.query(User).get(user_id)
        self.assertTrue(confirmed_user.confirmed)

    async def test_update_avatar(self):
        user = User()
        user.avatar = 'old_avatar'
        avatar_url = 'test_url'
        result = await update_avatar(email=user.email, url=avatar_url, db=self.session)
        self.assertEqual(avatar_url, result.avatar)


if __name__ == '__main__':
    unittest.main()
