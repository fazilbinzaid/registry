

# rest_framework
from rest_framework import serializers

# custom imports
from .models import *


class RoleSerializer(serializers.ModelSerializer):
    """
    Serializer for model Role.
    """
    class Meta:
        model = Role
        fields = [f.name for f in model._meta.fields]
