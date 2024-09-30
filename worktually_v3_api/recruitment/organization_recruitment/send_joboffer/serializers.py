import os
import requests
from rest_framework import serializers
from recruitment.models import JobOffer, Candidate
from job_seekers.models import JobSeeker
from recruitment.tasks import send_job_offer_notification


class JobOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobOffer
        fields = [
            "job_post_id",
            "candidate_id",
            "currency",
            "amount",
            "counter_amount",
            "counter_by",
            "expired_at",
        ]

    def validate_candidate_id(self, value):
        # Fetch candidate directly from the database
        try:
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

        # Attach job_seeker_id to the serializer context for later use
        self.context["job_seeker_email"] = job_seeker.email
        self.context["job_seeker_first_name"] = job_seeker.first_name

        return value

    def create(self, validated_data):
        job_offer = super().create(validated_data)

        # Retrieve job seeker details from the context
        job_seeker_email = self.context.get("job_seeker_email")
        job_seeker_first_name = self.context.get("job_seeker_first_name")

        if job_seeker_email:
            # Call the Celery task to send an email
            send_job_offer_notification.delay(
                job_seeker_email,
                job_seeker_first_name,
                job_offer.job_post_id,
                job_offer.amount,
                job_offer.currency,
            )

        return job_offer


class JobOfferUpdateSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=45, required=False)
    counter_amount = serializers.IntegerField(required=False)
    rejected_reason = serializers.CharField(
        max_length=1000, required=False, allow_blank=True
    )

    def validate(self, data):
        if data.get("status") == "Rejected" and not data.get("rejected_reason"):
            raise serializers.ValidationError(
                "Rejected reason is required when rejecting a job offer."
            )
        return data
