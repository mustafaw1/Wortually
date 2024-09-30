from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import AcceptRejectInterviewSerializer, RescheduleInterviewSerializer
from rest_framework import serializers
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from worktually_v3_api.custom_jwt.jwt import JobSeekerJWTAuthentication
from rest_framework.permissions import IsAuthenticated


class AcceptRejectInterviewView(APIView):
    authentication_classes = [JobSeekerJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=AcceptRejectInterviewSerializer,
        responses={
            200: openapi.Response("Success", AcceptRejectInterviewSerializer),
            400: "Validation Error",
            404: "Interview not found",
        },
    )
    def post(self, request, pk):
        serializer = AcceptRejectInterviewSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data

            try:
                result = serializer.update_interview_status(pk, validated_data)
                return Response(
                    {"message": "Success", "data": result},
                    status=status.HTTP_200_OK,
                )
            except serializers.ValidationError as e:
                return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RescheduleInterviewView(APIView):
    authentication_classes = [JobSeekerJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=RescheduleInterviewSerializer,
        responses={
            200: openapi.Response("Success", RescheduleInterviewSerializer),
            400: "Validation Error",
            404: "Interview not found",
        },
    )
    def post(self, request, pk):
        serializer = RescheduleInterviewSerializer(data=request.data)
        if serializer.is_valid():
            try:
                result = serializer.reschedule_interview(pk, serializer.validated_data)
                return Response(
                    {"message": "Success", "data": result}, status=status.HTTP_200_OK
                )
            except serializers.ValidationError as e:
                return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
