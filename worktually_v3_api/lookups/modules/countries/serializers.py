from rest_framework import serializers
from lookups.models import Country


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ["id", "name", "iso3", "iso2", "phone_code", "capital", "currency"]
