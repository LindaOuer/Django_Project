from rest_framework import serializers
from hub.models import Student


class StudentSerializer(serializers.Serializer):
    lastName = serializers.CharField(max_length=30)
    firstName = serializers.CharField(max_length=30)
    email = serializers.EmailField()
