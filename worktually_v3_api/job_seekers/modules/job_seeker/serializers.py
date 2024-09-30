from rest_framework import serializers
from .models import JobSeeker
from lookups.modules.cities.serializers import CitySerializer
from lookups.modules.countries.serializers import CountrySerializer
from lookups.modules.states.serializers import StateSerializer

class BasicProfileSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)
    city = CitySerializer(read_only=True)
    state = StateSerializer(read_only=True)

    class Meta:
        model = JobSeeker
        fields = [
            "id",
            "profile_picture_url",
            "first_name",
            "last_name",
            "email",
            "phone",
            "birth_date",
            "gender",
            "id_number",        
            "timezone",
            "country",
            "city",
            "state",
            "status",
        ]


class ProfilePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSeeker
        fields = ['profile_picture_url']

    def validate(self, data):
        """
        Ensure that either 'profile_picture' or 'profile_picture_url' is provided, but not both.
        """
        profile_picture = data.get('profile_picture')
        profile_picture_url = data.get('profile_picture_url')

        if profile_picture and profile_picture_url:
            raise serializers.ValidationError("Provide either a profile picture or a profile picture URL, not both.")
        return data


