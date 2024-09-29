from django_countries.data import COUNTRIES
from django_countries.serializer_fields import CountryField
from rest_framework import serializers

from cafe.models import Cafe, EmployeeCafe
from common.constants import MAX_UPLOAD_FILE_SIZE, MIME_TYPES
from common.utils.files import validate_file


class EmployeeCafeSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="cafe.id")
    name = serializers.UUIDField(source="cafe.name")

    class Meta:
        model = EmployeeCafe
        fields = ["id", "name"]


class CafeSerializer(serializers.ModelSerializer):
    location = CountryField()

    class Meta:
        model = Cafe
        fields = ["id", "name", "description", "location"]
        read_only_fields = ["id"]


class CafeListSerializer(serializers.ModelSerializer):
    location = serializers.SerializerMethodField()
    employees_count = serializers.IntegerField()
    logo = serializers.ImageField()

    def get_location(self, obj: Cafe):
        return COUNTRIES[obj.location] if obj.location else None

    class Meta:
        model = Cafe
        fields = ["id", "name", "description", "location", "employees_count", "logo"]
        read_only_fields = ["id", "logo"]


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
