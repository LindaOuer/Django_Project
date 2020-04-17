from rest_framework import serializers
from hub.models import Project


class ProjectSerializer(serializers.Serializer):
    project_name = serializers.CharField(max_length=30)
    duration = serializers.IntegerField()
    allocated_time = serializers.IntegerField()
