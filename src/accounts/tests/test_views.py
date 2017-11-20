import pytest
from mixer.backend.django import mixer
from django.test import Client
from django.core.urlresolvers import reverse
from datetime import datetime, timedelta
from django.utils import timezone

# rest_framework
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token

# custom imports
from src.accounts.models import Account
from src.abstract.tests import BaseViewSetTestMixin
from src.utils.models import Role

pytestmark = pytest.mark.django_db


class TestAuthTokenView:
    """
    Tests whether auth-token is retrieved properly.
    """
    def test_token_request(self):
        client = Client()
        user = Account.objects.create_user(email='test@gmail.com', password='1234')
        user.is_active = True
        user.save()
        response = client.post('/api/login/', {
            'email':'test@gmail.com', 'password':'1234'
        })
        response.render()
        assert response.status_code == 200, "Should retrieve the token."
        expected_msg = "User Authenticated"
        assert response.json()['msg'] == expected_msg
        assert response.json()['success']

    def test_wrong_email_login_check(self):

        """
        Tests a user cannot login with wrong email address.
        """
        client = Client()
        user = Account.objects.create_user(email='testnew@gmail.com', password='1234')
        user.is_active = True
        user.save()
        response = client.post('/api/login/', {
            'email': 'testnew1@gmail.com', 'password': '1234'
        })
        response.render()
        assert response.status_code == 200
        expected_msg = "Error in User Credentials Provided."
        assert response.json()['msg'] == expected_msg
        assert response.json()['success'] == False

class TestForgotPasswordView:
    """
    Tests whether Reset Password View is functioning properly.
    """

    def test_forgot_password_success(self):

        """
        Tests whether the view responds as written.
        """
        client = Client()
        user = mixer.blend(Account, email='testuserlegit@gmail.com', password='vja1234')
        url = '/api/forgot-password/'
        data = {
            'email': 'testuserlegit@gmail.com',
        }
        response = client.post(url, data, format='json')
        response.render()
        assert response.status_code == 200
        expected_msg = "Email sent. Please check your inbox"
        assert response.json()['msg'] == expected_msg

    def test_forgot_password_fail(self):
        """
        Tests whether the view responds as written.
        """
        client = Client()
        url = '/api/forgot-password/'
        data = {
            'email': 'faketestuser@gmail.com'
        }
        response = client.post(url, data, format='json')
        response.render()
        assert response.status_code == 200
        expected_msg = "No such User"
        assert response.json()['msg'] == expected_msg


class TestResetPasswordViewSet:
    """
    Test for Reset Password View after clicking on the link in email.
    """

    def test_reset_password_success(self):
        """
        Tests whether password can be reset using the view.
        """
        client = Client()
        user = mixer.blend(Account, email='faketestuser@gmail.com', password='vja1234')
        import hashlib
        from django.conf import settings
        email = 'faketestuser@gmail.com'.encode('utf-8')
        secret_key = settings.SECRET_KEY.encode('utf-8')
        key = hashlib.sha512(email+secret_key).hexdigest()

        url = reverse('accounts:reset-password', kwargs={'pk': user.pk, 'key': key})
        data = {
            'new_password': 'fakenewpassword'
        }
        response = client.post(url, data, format='json')
        response.render()

        assert response.status_code == 200
        expected_msg = "Password Updated"
        assert response.json()['msg'] == expected_msg

    def test_reset_password_fail(self):
        """
        Tests whether password cannot be reset using random key.
        """
        client = Client()
        user = mixer.blend(Account, email='testuser1@gmail.com', password='vja1234')
        url = reverse('accounts:reset-password', kwargs={'pk':user.pk, 'key': "blaablaableebleebloobloo"})
        data = {
            'new_password': 'fakenewpassword'
        }
        response = client.post(url, data, format='json')
        response.render()

        assert response.status_code == 200
        expected_msg = "Invalid / Expired Key"
        assert response.json()['msg'] == expected_msg


class TestChangePasswordView(APITestCase):
    """
    Test for change password view
    """
    def setUp(self):
        self.client = APIClient()

    def test_change_password_success(self):
        """
        Tests whether password can be changed from the view.
        """
        client = Client()
        user = Account.objects.create(email='exampleuser@gmail.com', password='vja1234')
        url = reverse('accounts:change-password')
        data = {
            'current_password': 'vja1234',
            'new_password': 'newpassword1234'
        }
        assert user.check_password(data['current_password'])

        self.client.force_authenticate(user=user)
        response = self.client.post(url, data, format='json')
        response.render()

        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        expected_msg = "Password has been successfully Updated."
        assert expected_msg == response_data['msg']
        assert response_data['success']

        user.refresh_from_db()
        assert user.check_password(data['new_password'])


class TestValidateAuthTokenView(APITestCase):
    """
    Test for Validate auth token view.
    """

    def setUp(self):
        self.client = APIClient()

    def test_validate_auth_token_view(self):
        """
        Tests whether view validates auth token.
        """
        admin = Account.objects.create(email='admin@app.com', password='vja1234')
        url = reverse('accounts:validate-auth-token')
        data = {
            'token': admin.auth_token.key
        }

        response = self.client.post(url, data, format='json')
        response.render()

        self.assertEqual(response.status_code, 200)
        expected_msg = "Token validated."
        assert response.json()['success']
        assert expected_msg == response.json()['msg']


class TestAccountViewSet(BaseViewSetTestMixin, APITestCase):

    def setUp(self):
        self.namespace = 'accounts'
        self.url_name = 'users'
        self.url_base = "{}:{}".format(self.namespace, self.url_name)
        self.role_A, c = Role.objects.get_or_create(code='A')
        self.admin = mixer.blend(Account, role=self.role_A)
        self.user = self.item = self.admin
        self.client = APIClient()

        self.post_data = {
            "email" : "testuser@gmail.com",
            "password" : "vjardtapp",
            "full_name" : "Test User",
            "phone_number" : "9995311436",
            "role" : self.role_A.id,
        }

        self.update_data = {
            "id" : self.user.id,
            "email" : "testuser@gmail.com",
            "password": self.user.password,
            "full_name" : "New Test User",
            "phone_number" : "9567157674",
            "role" : 1,
        }


    def test_check_unique_email(self):

        """ Tests whether email address of each user is unique. """

        url = reverse(self.url_base + '-list')
        account = mixer.blend(Account, email='test1@gmail.com', role__code='I')
        self.post_data['email'] = 'test1@gmail.com'
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, self.post_data, format='json')

        response.render()
        self.assertEqual(response.status_code, 400)
