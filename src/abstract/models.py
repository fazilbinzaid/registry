from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.contenttypes.models import ContentType

# custom imports
from .utils import *

# Create your models here.


class BaseTrackingModel(models.Model):
    """
    Abstract base model for every table used in this project.
    """
    created_at = models.DateTimeField(default=timezone.now)
    created_on = models.DateField(default=today)
    edited_at = models.DateTimeField(auto_now=True)
    edited_on = models.DateField(auto_now=True)

    class Meta:
        abstract = True
