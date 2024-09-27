from django_countries.serializer_fields import CountryField
from rest_framework import serializers

from cafe.models import Cafe
from common.constants import MAX_UPLOAD_FILE_SIZE, MIME_TYPES
from common.utils.files import validate_file


class CafeSerializer(serializers.ModelSerializer):
    location = CountryField()

    class Meta:
        model = Cafe
        fields = ["id", "name", "description", "location"]
        read_only_fields = ["id"]


class CafeListSerializer(serializers.ModelSerializer):
    location = CountryField()
    employees_count = serializers.IntegerField()

    class Meta:
        model = Cafe
        fields = ["id", "name", "description", "location", "employees_count"]
        read_only_fields = ["id"]


class CafeLogoSerializer(serializers.ModelSerializer):
    logo = serializers.ImageField()

    def validate(self, attrs):
        data = super().validate(attrs)
        file_obj = data.get("logo")
        if file_obj:
            validate_file(
                file_obj,
                MAX_UPLOAD_FILE_SIZE,
                MIME_TYPES,
            )
        return data

    class Meta:
        model = Cafe
        fields = ["id", "logo"]
        read_only_fields = ["id"]
        extra_kwargs = {"logo": {"required": False}}


class CafeCountrySerializer(serializers.Serializer):
    label = serializers.CharField()
    value = serializers.CharField()
