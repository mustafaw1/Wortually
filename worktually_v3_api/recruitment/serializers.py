import os
import requests
from rest_framework import serializers
from .models import JobPost


class JobPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPost
        fields = "__all__"

    def validate_organization_id(self, value):
        api_key = os.getenv("API_KEY")
        headers = {"Authorization": f"Api-Key {api_key}"}

        response = requests.get(
            f"https://dev3-api.worktually.com/api/organizations/{value}/",
            headers=headers,
        )

        if response.status_code != 200:
            raise serializers.ValidationError(
                "Organization with this ID does not exist."
            )

        return value

    def create(self, validated_data):
        # Directly creating the object without checking foreign key constraints
        return JobPost.objects.create(**validated_data)
