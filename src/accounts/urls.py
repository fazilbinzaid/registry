from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

# custom imports
from .views import *

router = DefaultRouter()
router.register(r'users', AccountViewSet, base_name='users')

urlpatterns = [

    url(r'^login/', Login.as_view(), name='user_login'),
    url(r'^logout/', user_logout, name='user_logout'),
    url(r'^forgot-password/', ForgotPassword.as_view(), name='forgot-password'),
    url(r'^reset-password/(?P<pk>\d+)/(?P<key>[-\w\d]+)/$', ResetPassword.as_view(), name='reset-password'),
    url(r'^change-password/$', ChangePasswordView.as_view(), name='change-password'),

    # router urls
    url(r'^', include(router.urls)),

            ]
