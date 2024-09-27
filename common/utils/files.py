import magic
from django.core.files import File
from rest_framework import serializers


def validate_file(
        file_obj: File,
        max_file_size: int,
        allowed_types: tuple,
) -> None:
    if file_obj.size > max_file_size:
        raise serializers.ValidationError(
            "File exceeded the size limit {}".format(max_file_size),
        )
    file_obj.seek(0)
    mime = magic.from_buffer(file_obj.read(2048), mime=True)
    if mime not in allowed_types:
        raise serializers.ValidationError(
            "Invalid type found {detected_type}. Allowed types are {allowed_types}".format(
                detected_type=mime,
                allowed_types=", ".join(allowed_types),
            ),
        )
