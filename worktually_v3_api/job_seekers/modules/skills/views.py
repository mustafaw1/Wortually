from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from job_seekers.modules.skills.models import Skills
from .serializers import SkillSerializer
from job_seekers.modules.skills.models import Skills, JobProfileSkill
from job_seekers.models import JobProfile
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from lookups.models import SkillCategory
from job_seekers.modules.skills.models import Skills
from job_seekers.modules.skills.serializers import (
    SkillSerializer,
    SkillCategorySerializer,
    UpdateJobProfileSkillsSerializer
)
from rest_framework.views import APIView
from worktually_v3_api.custom_jwt.jwt import JobSeekerJWTAuthentication


class AddSkillCategoryView(generics.CreateAPIView):
    authentication_classes = [JobSeekerJWTAuthentication]
    queryset = SkillCategory.objects.all()
    serializer_class = SkillCategorySerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=SkillCategorySerializer,
        responses={
            201: openapi.Response(
                "Skill category added successfully.", SkillCategorySerializer
            ),
            400: "Bad Request",
        },
        operation_description="Add a new skill category.",
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            skill_category = serializer.save()
            return Response(
                {
                    "status": "success",
                    "data": SkillCategorySerializer(skill_category).data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"status": "error", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class UpdateSkillCategoryView(generics.UpdateAPIView):
    authentication_classes = [JobSeekerJWTAuthentication]
    queryset = SkillCategory.objects.all()
    serializer_class = SkillCategorySerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"

    @swagger_auto_schema(
        request_body=SkillCategorySerializer,
        responses={
            200: openapi.Response(
                "Skill category updated successfully.", SkillCategorySerializer
            ),
            400: "Bad Request",
            404: "Not Found",
        },
        operation_description="Update an existing skill category.",
    )
    def put(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            skill_category = serializer.save()
            return Response(
                {
                    "status": "success",
                    "data": SkillCategorySerializer(skill_category).data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"status": "error", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class DeleteSkillCategoryView(generics.DestroyAPIView):
    authentication_classes = [JobSeekerJWTAuthentication]
    queryset = SkillCategory.objects.all()
    serializer_class = SkillCategorySerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"

    @swagger_auto_schema(
        responses={
            204: "Skill category deleted successfully.",
            400: "Bad Request",
            404: "Not Found",
        },
        operation_description="Delete a skill category.",
    )
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"status": "success", "message": "Skill category deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )



class UpdateJobProfileSkillsView(APIView):
    authentication_classes = [JobSeekerJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'job_profile_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the job profile'),
                'categories': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'categoryId': openapi.Schema(type=openapi.TYPE_INTEGER, description='Category ID'),
                            'skillIds': openapi.Schema(
                                type=openapi.TYPE_ARRAY,
                                items=openapi.Schema(type=openapi.TYPE_INTEGER),
                                description='Array of skill IDs'
                            )
                        }
                    )
                )
            }
        ),
        responses={
            200: openapi.Response(
                description="Job Profile Skills updated successfully",
                examples={
                    "application/json": {
                        "message": "Job profile skills updated successfully."
                    }
                }
            ),
            400: "Bad Request",
            404: "Job profile or skills not found"
        },
        operation_description="Update job profile skills based on the provided category and skill data."
    )
    def put(self, request, *args, **kwargs):
        job_profile_id = request.data.get('job_profile_id')
        if not job_profile_id:
            return Response({"error": "Job profile ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            job_profile = JobProfile.objects.get(id=job_profile_id)
        except JobProfile.DoesNotExist:
            return Response({"error": "Job profile not found."}, status=status.HTTP_404_NOT_FOUND)

        categories = request.data.get('categories', [])
        for category in categories:
            category_id = category.get('categoryId')
            skill_ids = category.get('skillIds', [])

            existing_skills = JobProfileSkill.objects.filter(
                job_profile=job_profile, skill__skill_category_id=category_id
            )
            existing_skill_ids = set(existing_skills.values_list('skill_id', flat=True))

            new_skill_ids = set(skill_ids)
            skills_to_add = new_skill_ids - existing_skill_ids
            for skill_id in skills_to_add:
                try:
                    skill = Skills.objects.get(id=skill_id)
                    JobProfileSkill.objects.create(skill=skill, job_profile=job_profile)
                except Skills.DoesNotExist:
                    return Response({"error": "One or more skills not found."}, status=status.HTTP_404_NOT_FOUND)

            skills_to_remove = existing_skill_ids - new_skill_ids
            JobProfileSkill.objects.filter(
                job_profile=job_profile, skill_id__in=skills_to_remove
            ).delete()

        return Response({"message": "Job profile skills updated successfully."}, status=status.HTTP_200_OK)











