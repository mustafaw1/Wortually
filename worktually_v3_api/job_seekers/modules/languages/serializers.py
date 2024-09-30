from rest_framework import serializers
from .models import Language
from lookups.serializers import LanguagesSerializer
from lookups.models import Language as LookupLanguage

class LanguageSerializer(serializers.ModelSerializer):
    language = serializers.PrimaryKeyRelatedField(queryset=LookupLanguage.objects.all())
    language_details = LanguagesSerializer(source='language', read_only=True)
    class Meta:
        model = Language
        fields = ['id', 'language', 'proficiency',  'created_at', 'updated_at', 'language_details',]
        read_only_fields = ['job_seeker', 'created_at', 'updated_at']

    def create(self, validated_data):
        # Set the job_seeker to the logged-in user from the request context
        job_seeker = self.context['request'].user
        validated_data['job_seeker'] = job_seeker
        return super().create(validated_data)

