from django.db import models
from django.utils import timezone
from datetime import timedelta

# Create your models here.


def today():
    """
    Returns current timezone aware date.
    """
    return timezone.now().date()

def next_week_day():
    """
    Returns next week day from today.
    """
    return today() + timedelta(days=6)

def next_month_day():
    """
    Returns next month day from today.
    """
    return today() + timedelta(days=30)

def next_year_day():
    """
    Returns next year day from today.
    """
    return today() + timedelta(days=365)
