import unittest
from unittest.mock import MagicMock
from libgravatar import Gravatar
from sqlalchemy.orm import Session
from src.database.models import User
from src.schemas import UserModel
from src.repository.users import (
    get_user_by_email,
    create_user,
    update_token,
    confirmed_email,
    update_avatar,
)

class TestUserFunctions(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)

    async def test_get_user_by_email(self):
        user = User(id=1, email="test@example.com")
        self.session.query().filter().first.return_value = user
        result = await get_user_by_email(email="test@example.com", db=self.session)
        self.assertEqual(result, user)

    async def test_get_user_by_email_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_user_by_email(email="nonexistent@example.com", db=self.session)
        self.assertIsNone(result)

    async def test_create_user(self):
        user_data = UserModel(
            username="testuser",
            email="test@example.com",
            password="password123",
        )
        gravatar_mock = MagicMock(spec=Gravatar)
        gravatar_mock.get_image.return_value = "http://example.com/avatar.jpg"
        with unittest.mock.patch('libgravatar.Gravatar', return_value=gravatar_mock):
            new_user = User(**user_data.dict(), avatar="http://example.com/avatar.jpg")
            self.session.add(new_user)
            self.session.commit.return_value = None
            self.session.refresh(new_user)
            result = await create_user(body=user_data, db=self.session)
            self.assertEqual(result, new_user)

    async def test_create_user_with_gravatar_error(self):
        user_data = UserModel(
            username="testuser",
            email="test@example.com",
            password="password123",
        )
        gravatar_mock = MagicMock(spec=Gravatar)
        gravatar_mock.get_image.side_effect = Exception("Gravatar error")
        with unittest.mock.patch('libgravatar.Gravatar', return_value=gravatar_mock):
            new_user = User(**user_data.dict(), avatar=None)
            self.session.add(new_user)
            self.session.commit.return_value = None
            self.session.refresh(new_user)
            result = await create_user(body=user_data, db=self.session)
            self.assertEqual(result, new_user)

    async def test_update_token(self):
        user = User(id=1, username="testuser", email="test@example.com", password="password123")
        self.session.commit.return_value = None
        update_token_value = "new_token"
        user.refresh_token = update_token_value
        result = await update_token(user=user, token=update_token_value, db=self.session)
        self.assertIsNone(result)
        self.assertEqual(user.refresh_token, update_token_value)

    async def test_confirmed_email(self):
        user = User(id=1, username="testuser", email="test@example.com", password="password123")
        user.confirmed = False
        self.session.commit.return_value = None
        result = await confirmed_email(email="test@example.com", db=self.session)
        self.assertIsNone(result)
        self.assertTrue(user.confirmed)

    async def test_update_avatar(self):
        user = User(id=1, username="testuser", email="test@example.com", password="password123")
        new_avatar_url = "http://example.com/new_avatar.jpg"
        self.session.commit.return_value = None
        user.avatar = new_avatar_url
        result = await update_avatar(email="test@example.com", url=new_avatar_url, db=self.session)
        self.assertEqual(result, user)

if __name__ == '__main__':
    unittest.main()
