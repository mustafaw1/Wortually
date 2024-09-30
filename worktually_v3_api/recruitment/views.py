from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import JobPost
from .serializers import JobPostSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from worktually_v3_api.custom_jwt.jwt import EmployeeJWTAuthentication


class JobPostCreateView(APIView):
    authentication_classes = [EmployeeJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=JobPostSerializer,
        responses={
            201: openapi.Response("Success", JobPostSerializer),
            400: "Bad Request",
        },
    )
    def post(self, request):
        serializer = JobPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Success", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JobPostEditView(APIView):
    authentication_classes = [EmployeeJWTAuthentication]

    @swagger_auto_schema(
        request_body=JobPostSerializer,
        responses={
            200: openapi.Response("Success", JobPostSerializer),
            400: "Bad Request",
            404: "Not Found",
        },
    )
    def put(self, request, pk):
        try:
            job_post = JobPost.objects.get(pk=pk)
        except JobPost.DoesNotExist:
            return Response({"message": "Not Found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = JobPostSerializer(job_post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Success", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JobPostDeleteView(APIView):
    authentication_classes = [EmployeeJWTAuthentication]

    @swagger_auto_schema(responses={204: "No Content", 404: "Not Found"})
    def delete(self, request, pk):
        try:
            job_post = JobPost.objects.get(pk=pk)
        except JobPost.DoesNotExist:
            return Response({"message": "Not Found"}, status=status.HTTP_404_NOT_FOUND)

        job_post.delete()
        return Response({"message": "Success"}, status=status.HTTP_204_NO_CONTENT)


class JobPostListView(generics.ListAPIView):
    authentication_classes = [EmployeeJWTAuthentication]
    queryset = JobPost.objects.all()
    serializer_class = JobPostSerializer

    @swagger_auto_schema(
        operation_description="Retrieve all job posts",
        responses={
            200: openapi.Response("Success", JobPostSerializer(many=True)),
            400: "Bad Request",
        },
    )
    def get(self, request, *args, **kwargs):
        job_posts = self.get_queryset()
        serializer = self.get_serializer(job_posts, many=True)
        return Response(
            {"message": "Success", "data": serializer.data}, status=status.HTTP_200_OK
        )


class JobPostDetailView(APIView):
    authentication_classes = [EmployeeJWTAuthentication]

    @swagger_auto_schema(
        responses={
            200: openapi.Response("Success", JobPostSerializer),
            404: "Not Found",
        }
    )
    def get(self, request, pk):
        try:
            job_post = JobPost.objects.get(pk=pk)
        except JobPost.DoesNotExist:
            return Response({"message": "Not Found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = JobPostSerializer(job_post)
        return Response(
            {"message": "Success", "data": serializer.data}, status=status.HTTP_200_OK
        )
