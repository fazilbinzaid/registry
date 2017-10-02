import random
from datetime import timedelta
from collections import defaultdict

from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from django.core.validators import RegexValidator, MinLengthValidator
from django.db.models import Q, Sum, Count
from django.db.models.functions import Coalesce

# rest_framework
from rest_framework.authtoken.models import Token

# custom imports
from .managers import *
from src.utils.models import *
from src.abstract.utils import *
from src.abstract.models import *


class Account(AbstractBaseUser):
    """
    Custom Auth User model.
    Provides all the basic features of Django's auth User model, plus some
    required custom functionalities.
    """

    phone_number_regex_validator = RegexValidator(regex=r'^[0-9]{10}$', message='Invalid Phone Number.')

    username = models.CharField(unique=True)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=10, validators=[phone_number_regex_validator, MinLengthValidator(10)])
    role = models.ForeignKey(Role, related_name='accounts')

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    date_of_joining = models.DateField(default=today)

    leaves_taken = models.PositiveIntegerField(default=0, blank=True)
    halfday_leaves_taken=models.FloatField(default=0.0, blank=True)
    initial_login = models.BooleanField(default=True)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        ordering = ('-id', )

    def clean(self, *args, **kwargs):
        super(Account, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):

        self.clean(*args)
        super(Account, self).save(*args, **kwargs)

    @property
    def leave_count(self):
        return (self.leaves_taken + self.halfday_leaves_taken)

    @property
    def username(self):
        return self.full_name

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.full_name

    def has_module_perms(self, temp):
        return True

    def has_perm(self, temp):
        return True

    def __str__(self):
        return self.email
