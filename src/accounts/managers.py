from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.db.models import Q

# custom imports
from src.utils.models import Role


class AccountManager(BaseUserManager):
    """
    Custom Base Manager for Custom User Model (Account).
    Provides all the required functionalities for the AUTH_USER_MODEL.
    """
    use_in_migrations = True

    def _create_user(self, email, password, **kwargs):
        """
        Function to create a user with given arguments.
        """
        if not email:
            raise ValueError('Users must have a valid email address and provide a username.')
        email = self.normalize_email(email)
        account = self.model(email=email, password=password, **kwargs)
        account.set_password(password)
        account.role, created = Role.objects.get_or_create(code='I', desc='Inactive')
        account.is_active = True
        account.save()
        return account

    def create_user(self, email, password=None, **kwargs):
        """
        Top level function which calls to be called upon when a user is to be created.
        """
        kwargs.setdefault('is_superuser', False)
        return self._create_user(email, password, **kwargs)

    def create_superuser(self, email, password, **kwargs):
        """
        Function to create a new superuser with all permissions.
        """
        account = self._create_user(email, password, **kwargs)
        account.is_active = True
        account.is_superuser = True
        account.is_admin = True
        account.is_staff = True
        account.role, created = Role.objects.get_or_create(code='A')
        account.save()

        return account

    def create(self, **kwargs):
        """
        Overrided model's create method inorder to provide better integration with testing
        utilities like mixer, pytest and command level user creation.
        """
        email = kwargs.pop('email')
        password = kwargs.pop('password')
        user = self.create_user(email, password)
        for key, value in kwargs.items():
            setattr(user, key, value)
        user.save()
        return user

    def get_by_email(self, email):
        """
        Returns the user with the email provided.
        """
        return self.get_queryset().get(email=email)

    def _check_unique_email(self, email):
        """
        Checks whether a given email is unique or not.
        Raises validation error when email is already existing, else return True.
        """
        try:
            self.get_queryset().get(email=email)
            raise ValueError("This email is already registered.")
        except self.model.DoesNotExist:
            return True
