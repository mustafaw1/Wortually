from rest_framework import serializers
from .models import ScreeningInterviewTemplate, JobProfileInterview


class ScreeningInterviewTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScreeningInterviewTemplate
        fields = "__all__"


class JobProfileInterviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobProfileInterview
        fields = "__all__"
