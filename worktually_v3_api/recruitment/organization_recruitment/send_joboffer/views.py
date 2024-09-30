from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from recruitment.models import JobOffer
from .serializers import JobOfferSerializer, JobOfferUpdateSerializer
from rest_framework.permissions import IsAuthenticated
from worktually_v3_api.custom_jwt.jwt import EmployeeJWTAuthentication


class SendJobOfferView(APIView):
    authentication_classes = [EmployeeJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=JobOfferSerializer,
        responses={
            201: openapi.Response("Created", JobOfferSerializer),
            400: "Bad Request",
        },
    )
    def post(self, request):
        serializer = JobOfferSerializer(data=request.data)
        if serializer.is_valid():
            job_offer = serializer.save()
            return Response(
                {"message": "Job offer sent successfully.", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"errors": serializer.errors, "message": "There were validation errors."},
            status=status.HTTP_400_BAD_REQUEST,
        )


class RetrieveJobOfferView(APIView):
    authentication_classes = [EmployeeJWTAuthentication]

    @swagger_auto_schema(
        responses={200: JobOfferSerializer(), 404: "Job offer not found"}
    )
    def get(self, request, job_offer_id):
        try:
            job_offer = JobOffer.objects.get(id=job_offer_id)
        except JobOffer.DoesNotExist:
            return Response(
                {"error": "Job offer not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = JobOfferSerializer(job_offer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=JobOfferUpdateSerializer,
        responses={
            200: "Job offer updated successfully.",
            400: "Bad Request",
            404: "Not Found",
        },
    )
    def patch(self, request, job_offer_id):
        try:
            job_offer = JobOffer.objects.get(id=job_offer_id)
        except JobOffer.DoesNotExist:
            return Response(
                {"error": "Job offer not found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = JobOfferUpdateSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            for key, value in serializer.validated_data.items():
                setattr(job_offer, key, value)
            job_offer.save()
            return Response(
                {"message": "Job offer updated successfully."},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
