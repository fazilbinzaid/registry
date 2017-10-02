

# rest_framework
from rest_framework import serializers

# custom imports
from .models import *


class AccountSerializer(serializers.ModelSerializer):
    """
    Custom serializer class for model Account.
    """
    password = serializers.CharField(style={'input_type': 'password'}, required=False, write_only=True)

    class Meta:
        model = Account
        fields = [f.name for f in model._meta.fields]

