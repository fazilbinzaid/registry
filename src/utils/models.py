from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from django.core.validators import RegexValidator

# custom imports
from .managers import *
from src.abstract.models import *

# Create your models here.

class Role(BaseTrackingModel):
    """
    Model for storing details of User roles in the project.
    """

    code = models.CharField(max_length=1, default='A', unique=True)
    desc = models.CharField(max_length=20)
    payment_amount = models.PositiveIntegerField(default=0)
    increment = models.PositiveIntegerField(default=0)
    leave_limit = models.PositiveIntegerField(default=0)

    objects = RoleQuerySet.as_manager()

    def __str__(self):
        return "{}-{}".format(self.code, self.desc)
