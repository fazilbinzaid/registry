from django.conf.urls import url, include

# rest_framework
from rest_framework.routers import DefaultRouter

# custom imports
from .views import *

router = DefaultRouter()
router.register(r'users', AccountViewSet, base_name='users')

urlpatterns = [

    url(r'^login/', LoginView.as_view(), name='user_login'),
    url(r'^logout/', user_logout_view, name='user_logout'),
    url(r'^forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    url(r'^reset-password/(?P<pk>\d+)/(?P<key>[-\w\d]+)/$', ResetPasswordView.as_view(), name='reset-password'),
    url(r'^change-password/$', ChangePasswordView.as_view(), name='change-password'),
    url(r'^validate-auth-token/$', ValidateAuthTokenView.as_view(), name='validate-auth-token'),

    # router urls
    url(r'^', include(router.urls)),

]
