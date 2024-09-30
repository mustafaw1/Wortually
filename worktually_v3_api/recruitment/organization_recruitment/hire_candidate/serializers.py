import requests
import os
from datetime import date
from rest_framework import serializers
from recruitment.models import JobOffer, JobPost, Candidate


class HireCandidateSerializer(serializers.Serializer):
    job_post_id = serializers.IntegerField()
    candidate_id = serializers.IntegerField()
    job_offer_id = serializers.IntegerField()
    hire_date = serializers.DateField()

    def validate_job_post_id(self, value):
        if not JobPost.objects.filter(id=value).exists():
            raise serializers.ValidationError("Job post does not exist.")
        return value

    def validate_candidate_id(self, value):
        # Directly check if the candidate exists in the database
        if not Candidate.objects.filter(id=value).exists():
            raise serializers.ValidationError("Candidate does not exist.")
        return value

    def validate(self, data):
        job_offer_id = data.get("job_offer_id")
        try:
            job_offer = JobOffer.objects.get(id=job_offer_id)
            if job_offer.status != "Accept":
                raise serializers.ValidationError("The job offer is not accepted.")
        except JobOffer.DoesNotExist:
            raise serializers.ValidationError("Job offer does not exist.")

        data["job_offer"] = job_offer
        return data

    def validate_hire_date(self, value):
        if value < date.today():
            raise serializers.ValidationError("Hire date cannot be in the past.")
        return value

    def create(self, validated_data):
        candidate_id = validated_data["candidate_id"]
        hire_date = validated_data["hire_date"]

        # Fetch the candidate instance and update its status to 'Hired'
        candidate = Candidate.objects.get(id=candidate_id)
        candidate.status = "Hired"
        candidate.hire_date = (
            hire_date  # Assuming there's a hire_date field in Candidate
        )
        candidate.save()

        # Return the validated data or any other relevant information
        return {
            "job_post_id": validated_data["job_post_id"],
            "candidate_id": candidate_id,
            "job_offer_id": validated_data["job_offer_id"],
            "hire_date": hire_date,
            "status": candidate.status,
        }
