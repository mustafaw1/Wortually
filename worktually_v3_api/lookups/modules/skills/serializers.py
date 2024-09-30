from rest_framework import serializers
from lookups.models import SkillCategory, Skills

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skills
        fields = ['id', 'name',  'created_at', 'updated_at']

class SkillCategorySerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)  # This will include all related skills

    class Meta:
        model = SkillCategory
        fields = ['id', 'name', 'skills', 'created_at', 'updated_at']  # Include any other fields needed
