from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import HireCandidateSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from worktually_v3_api.custom_jwt.jwt import EmployeeJWTAuthentication


class HireCandidateView(APIView):
    authentication_classes = [EmployeeJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=HireCandidateSerializer,
        responses={
            200: openapi.Response("Candidate hired successfully."),
            400: "Bad Request",
            404: "Not Found",
        },
    )
    def post(self, request):
        serializer = HireCandidateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": " success"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
