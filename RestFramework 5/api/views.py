from rest_framework import viewsets

from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

from hub.models import Project
from .serializers import ProjectSerializer


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.creator == request.user


class ProjectViewSet(viewsets.ModelViewSet):
    # queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (IsOwner,)

    # Ensure a user sees only its projects
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Project.objects.filter(creator=user)
        raise PermissionDenied()

    # Set user as creator of a project.
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
