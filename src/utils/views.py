from django.shortcuts import render

# rest_framework
from rest_framework import viewsets

# custom imports
from .models import *
from .serializers import *

# Create your views here.


class RoleViewSet(viewsets.ModelViewSet):
    """
    View for accessing Role details.
    Provides 'list', 'retrieve', 'create', 'update' & 'delete' methods.
    Permission level only for partners/HR.
    """
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
