from rest_framework import serializers
from recruitment.models import JobPost


class JobSearchSerializer(serializers.Serializer):
    job_title_id = serializers.IntegerField()

    def validate_job_title_id(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Job title ID must be a positive integer."
            )
        return value

    def search_jobs(self, job_title_id):
        # Query the database
        job_posts = JobPost.objects.filter(job_title_id=job_title_id)

        if not job_posts.exists():
            raise serializers.ValidationError(
                "No job posts found for the given job title ID."
            )

        return job_posts
