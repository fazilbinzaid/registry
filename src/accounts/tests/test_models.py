import pytest
from mixer.backend.django import mixer

# rest_framework
from rest_framework.test import APITestCase, APIClient

# custom imports
from src.accounts.models import *


pytestmark = pytest.mark.django_db


class TestAccount:
    """
    Test Case for Account model.
    """

    def test_account_model(self):
        """
        Tests the attributes of Account model.
        """
        obj = mixer.blend(Account)
        assert obj.__str__() == obj.email
