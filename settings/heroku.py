from .base import *

import dj_database_url


# TODO DEBUG = FALSE when production.
DEBUG = True

ALLOWED_HOSTS = ['*']

CORS_ORIGIN_ALLOW_ALL = True

DATABASES = {}

DATABASES['default'] = dj_database_url.config()

BASE_URL = "http://registry-django.herokuapp.com/"

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

REST_FRAMEWORK['PAGE_SIZE'] = 15

INTERNAL_IPS = [ '127.0.0.1' ]
