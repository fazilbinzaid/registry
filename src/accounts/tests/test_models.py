import pytest
from mixer.backend.django import mixer

# rest_framework
from rest_framework.test import APITestCase, APIClient

# custom imports
from src.accounts.models import *


pytestmark = pytest.mark.django_db


class TestAccount:

    def test_account_model(self):
        """
        Tests whether user is created.
        """
        obj = mixer.blend(Account, email='test@gmail.com', password='1234', full_name='test_user', role__code='P')
        assert type(obj) == Account, 'A User instance must be created.'
        assert obj.__str__() == 'test@gmail.com', 'object string must be email'
        assert obj.full_name == 'test_user', 'User full name must be the provided string.'
        assert obj.role.code == 'P', "User's role must be Partner."
        obj.save()

    def test_super_user(self):
        """
        Tests whether a superuser can be created with the model.
        """
        obj = Account.objects.create_superuser(
            email='test1@gmail.com',
            password='1234'
        )
        assert obj.is_superuser, "SuperUser must have superuser status."
        assert obj.is_admin, "SuperUser must have admin status."
        assert obj.is_staff, "SuperUser must have staff status."

    def test_token_generation(self):
        """
        Tests whether token is generated, when a user is created.
        """
        user = mixer.blend(Account, email='test2@gmail.com', password='1234')
        token = Token.objects.get(user=user)
        assert token.key, "Token must a key."

    def test_get_by_email(self):
        """
        Tests whether user can be got by email.
        """
        role = mixer.blend(Role)
        user1 = mixer.blend(Account, email="e1@app.com", role=role)
        user2 = mixer.blend(Account, email="e2@app.com", role=role)
        user = Account.objects.get_by_email("e1@app.com")

        assert user == user1
        assert user != user2

    def test_no_email(self):
        """
        Tests whether user can be created without email.
        """
        try:
            Account.objects.create_user(email=None, password='1234')
        except Exception as e:
            expected_msg = "Users must have a valid email address."
            assert expected_msg in e.args
