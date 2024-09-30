import requests
from rest_framework import serializers
from django.conf import settings
from recruitment.models import JobInterview
from rest_framework import serializers
from recruitment.models import JobInterview, Candidate, JobSeeker


class SendInterviewRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobInterview
        fields = "__all__"

    def validate_candidate_id(self, value):
        try:
            # Fetch the candidate directly from the database
            candidate = Candidate.objects.get(id=value)
        except Candidate.DoesNotExist:
            raise serializers.ValidationError("Candidate does not exist.")

        # Fetch job seeker details associated with the candidate
        try:
            job_seeker = JobSeeker.objects.get(id=candidate.job_seeker_id.id)
        except JobSeeker.DoesNotExist:
            raise serializers.ValidationError("Job seeker does not exist.")

        # Ensure email and first name are present
        if not job_seeker.first_name:
            raise serializers.ValidationError("Job seeker does not have a first name.")
        if not job_seeker.email:
            raise serializers.ValidationError("Job seeker does not have an email.")

        # Optionally, you can attach these details to the serializer's context or return them
        self.context["job_seeker_first_name"] = job_seeker.first_name
        self.context["job_seeker_email"] = job_seeker.email

        return value

    def create(self, validated_data):
        # Create the JobInterview instance
        job_interview = JobInterview.objects.create(**validated_data)

        # Retrieve job seeker details from the context
        job_seeker_email = self.context.get("job_seeker_email")

        return job_interview


class RescheduleInterviewSerializer(serializers.Serializer):
    reschedule_start_date = serializers.DateTimeField()
    reschedule_end_date = serializers.DateTimeField()
    reschedule_by = serializers.CharField(max_length=45)
    cancel_reason = serializers.CharField(
        max_length=255, required=False, allow_blank=True
    )

    def validate(self, data):
        if data["reschedule_start_date"] >= data["reschedule_end_date"]:
            raise serializers.ValidationError(
                "Reschedule start date must be before end date."
            )
        return data


class AcceptRejectInterviewSerializer(serializers.Serializer):
    status = serializers.ChoiceField(
        choices=[("Accepted", "Accepted"), ("Rejected", "Rejected")]
    )
    feedback = serializers.CharField(max_length=255, required=False)
    reschedule_start_date = serializers.DateTimeField(required=False)
    reschedule_end_date = serializers.DateTimeField(required=False)
    reschedule_by = serializers.CharField(max_length=45, required=False)
    cancel_reason = serializers.CharField(max_length=255, required=False)

    def validate(self, data):
        if "status" in data:
            if data["status"] not in ["Accepted", "Rejected", "Rescheduled"]:
                raise serializers.ValidationError(
                    "Invalid status. Must be 'Accepted', 'Rejected', or 'Rescheduled'."
                )
            if data["status"] == "Rejected" and "cancel_reason" not in data:
                raise serializers.ValidationError(
                    "cancel_reason is required when rejecting an interview."
                )

        return data
