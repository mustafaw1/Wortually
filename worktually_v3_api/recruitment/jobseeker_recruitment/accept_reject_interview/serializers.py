import os
import requests
from rest_framework import serializers
from django.utils.dateparse import parse_datetime
from recruitment.models import JobInterview


class InterviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobInterview
        fields = "__all__"


class AcceptRejectInterviewSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=45)
    cancel_reason = serializers.CharField(
        max_length=1000, required=False, allow_blank=True
    )

    def update_interview_status(self, interview_id, validated_data):
        try:
            # Fetch the interview instance
            interview = JobInterview.objects.get(id=interview_id)

            # Update the status and cancel_reason if provided
            interview.status = validated_data["status"]
            if "cancel_reason" in validated_data:
                interview.cancel_reason = validated_data["cancel_reason"]

            interview.save()

            # Serialize the interview instance
            serialized_interview = InterviewSerializer(interview).data
            return serialized_interview

        except JobInterview.DoesNotExist:
            raise serializers.ValidationError("Interview not found.")


class RescheduleInterviewSerializer(serializers.Serializer):
    reschedule_start_date = serializers.DateTimeField()
    reschedule_end_date = serializers.DateTimeField()
    reschedule_by = serializers.CharField(max_length=45)
    cancel_reason = serializers.CharField(max_length=100)

    def reschedule_interview(self, interview_id, validated_data):
        try:
            # Fetch the interview instance
            interview = JobInterview.objects.get(id=interview_id)

            # Update the interview with the rescheduled dates and other data
            interview.start_date = validated_data["reschedule_start_date"]
            interview.end_date = validated_data["reschedule_end_date"]
            interview.reschedule_by = validated_data["reschedule_by"]

            if "cancel_reason" in validated_data:
                interview.cancel_reason = validated_data["cancel_reason"]

            interview.save()

            # Serialize the interview instance
            serialized_interview = InterviewSerializer(interview).data
            return serialized_interview

        except JobInterview.DoesNotExist:
            raise serializers.ValidationError("Interview not found.")
