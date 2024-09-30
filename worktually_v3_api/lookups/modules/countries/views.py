from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from lookups.models import Country
from .serializers import CountrySerializer
from rest_framework.permissions import IsAuthenticated


class CountryView(APIView):
    @swagger_auto_schema(
        operation_description="Get all countries",
        responses={
            200: "Success",
        },
    )
    def get(self, request, *args, **kwargs):
        countries = Country.objects.all()
        serializer = CountrySerializer(countries, many=True)
        return Response(
            {
                "message": "success",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
