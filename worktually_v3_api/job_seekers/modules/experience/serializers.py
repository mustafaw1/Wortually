from rest_framework import serializers
from job_seekers.modules.experience.models import JobProfileExperience
from job_seekers.models import JobProfile

class JobProfileExperienceSerializer(serializers.ModelSerializer):
    job_profile = serializers.PrimaryKeyRelatedField(
        queryset=JobProfile.objects.all(),
        required=True
    )

    class Meta:
        model = JobProfileExperience
        fields = [
            "id",
            "job_profile",
            "company_name",
            "start_date",
            "end_date",
            "currently_working",
            "description",
            "country",
            "city",
        ]

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
