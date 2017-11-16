from django.conf.urls import url, include

# rest_framework
from rest_framework.routers import DefaultRouter

# custom imports
from .views import *


router = DefaultRouter()
router.register(r'roles', RoleViewSet, base_name='user-roles')

urlpatterns = [

    # router urls
    url(r'^', include(router.urls)),

]
