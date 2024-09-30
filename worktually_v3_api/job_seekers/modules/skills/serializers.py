from rest_framework import serializers
from job_seekers.modules.skills.models import Skills, JobProfileSkill
from lookups.models import SkillCategory
from job_seekers.models import JobProfile


class SkillCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillCategory
        fields = "__all__"


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skills
        fields = "__all__"


class AddSkillsToJobProfileSerializer(serializers.Serializer):
    job_profile_id = serializers.IntegerField()
    skill_ids = serializers.ListField(
        child=serializers.IntegerField(), allow_empty=False
    )


class JobProfileSkillSerializer(serializers.ModelSerializer):
    skill = SkillSerializer()
    class Meta:
        model = JobProfileSkill
        fields = ["skill"]




class UpdateJobProfileSkillsSerializer(serializers.Serializer):
    job_profile_id = serializers.IntegerField()
    categoryId = serializers.IntegerField(required=False)  # Not strictly necessary unless used for filtering
    skillIds = serializers.ListField(
        child=serializers.IntegerField(), allow_empty=False
    )

    def validate_skillIds(self, value):
        if not value:
            raise serializers.ValidationError("At least one skill ID must be provided.")
        return value
