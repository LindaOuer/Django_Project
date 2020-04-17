from rest_framework import viewsets, response, decorators, status

from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

from rest_framework_simplejwt.tokens import RefreshToken

from hub.models import Project
from .serializers import ProjectSerializer
from django.contrib.auth import get_user_model
from .serializers import UserCreateSerializer

User = get_user_model()


@decorators.api_view(["POST"])
@decorators.permission_classes([permissions.AllowAny])
def registration(request):
    serializer = UserCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return response.Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    user = serializer.save()
    refresh = RefreshToken.for_user(user)
    res = {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
    return response.Response(res, status.HTTP_201_CREATED)


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
