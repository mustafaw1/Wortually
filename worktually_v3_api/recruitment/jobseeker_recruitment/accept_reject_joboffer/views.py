from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from .serializers import AcceptRejectJobOfferSerializer
from rest_framework import serializers
from worktually_v3_api.custom_jwt.jwt import JobSeekerJWTAuthentication


class AcceptRejectJobOfferView(APIView):
    authentication_classes = [JobSeekerJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=AcceptRejectJobOfferSerializer,
        responses={
            200: "Job offer action processed successfully.",
            400: "Bad Request",
            404: "Not Found",
        },
    )
    def patch(self, request, job_offer_id):
        serializer = AcceptRejectJobOfferSerializer(data=request.data)
        if serializer.is_valid():
            try:
                response = serializer.update_job_offer(
                    job_offer_id, serializer.validated_data
                )
                return Response(
                    {"message": "success", "data": serializer.data},
                    status=status.HTTP_200_OK,
                )
            except serializers.ValidationError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
