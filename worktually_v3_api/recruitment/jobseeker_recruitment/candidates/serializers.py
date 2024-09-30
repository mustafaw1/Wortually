from rest_framework import serializers
from .models import Candidate


class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = "__all__"

    def update(self, instance, validated_data):
        instance.status = validated_data.get("status", instance.status)
        instance.expected_start_date = validated_data.get(
            "expected_start_date", instance.expected_start_date
        )
        instance.save()
        return instance
