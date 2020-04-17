from rest_framework import generics
from hub.models import Project
from .serializers import ProjectSerializer


class projects_List(generics.ListCreateAPIView):
    """
    Provides a get method handler.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class project_detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
