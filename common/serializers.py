from rest_framework import serializers


class FilterSerializer(serializers.Serializer):
    label = serializers.CharField()
    value = serializers.CharField()
