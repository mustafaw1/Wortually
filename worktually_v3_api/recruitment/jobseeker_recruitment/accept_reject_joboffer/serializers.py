import os
import requests
from rest_framework import serializers
from recruitment.models import JobOffer
from django.core.exceptions import ObjectDoesNotExist


class AcceptRejectJobOfferSerializer(serializers.Serializer):
    action = serializers.CharField(max_length=45)
    counter_amount = serializers.IntegerField(required=False, allow_null=True)
    rejected_reason = serializers.CharField(
        max_length=1000, required=False, allow_blank=True, allow_null=True
    )

    def validate_action(self, value):
        if value not in ["Accept", "Reject", "Counter"]:
            raise serializers.ValidationError("Invalid action value.")
        return value

    def validate(self, data):
        if data["action"] == "Reject" and not data.get("rejected_reason"):
            raise serializers.ValidationError(
                "Rejected reason is required when rejecting a job offer."
            )
        if data["action"] == "Counter" and not data.get("counter_amount"):
            raise serializers.ValidationError(
                "Counter amount is required when countering a job offer."
            )
        return data

    def update_job_offer(self, job_offer_id, validated_data):
        try:
            job_offer = JobOffer.objects.get(id=job_offer_id)

            # Update fields based on validated data
            job_offer.status = validated_data["action"].capitalize()

            if "counter_amount" in validated_data:
                job_offer.counter_amount = validated_data["counter_amount"]

            if "rejected_reason" in validated_data:
                job_offer.rejected_reason = validated_data["rejected_reason"]

            job_offer.save()

            return job_offer

        except JobOffer.DoesNotExist:
            raise serializers.ValidationError("Job offer not found.")
