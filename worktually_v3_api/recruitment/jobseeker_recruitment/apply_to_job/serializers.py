from rest_framework import serializers
from job_seekers.models import JobProfile
from recruitment.models import JobApplication
from job_seekers.tasks import send_job_application_notification


class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ["job_id", "job_seeker", "job_profile", "source"]

    def validate_job_profile(self, value):
        if not JobProfile.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Job profile does not exist.")
        return value

    def validate(self, data):
        # Perform basic validation, but no external API calls or complex queries
        return data

    def create(self, validated_data):
        job_application = super().create(validated_data)
        # Invoke task for sending notifications
        send_job_application_notification.delay(job_application.id)
        print(send_job_application_notification)
        # Update the 'is_applied' field to True
        job_application.is_applied = True
        job_application.save()
        return job_application
