from rest_framework import serializers
from .models import Education

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        ref_name = "JobSeekerEducationSerializer"
        fields = [
            "id",
            "degree_type",
            "discipline",
            "institute_name",
            "from_date",
            "to_date",
        ]
    
    # Automatically set job_seeker during creation
    def create(self, validated_data):
        # Automatically assign the job_seeker from the context request
        validated_data['job_seeker'] = self.context['request'].user
        return super().create(validated_data)