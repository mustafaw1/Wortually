from rest_framework import serializers
from lookups.models import State


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ["id", "name", "country"]
