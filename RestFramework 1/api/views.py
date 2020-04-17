from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from hub.models import Project
from .serializers import ProjectSerializer


def projects_List(request):
    """List all projects

    Arguments:
        request {HttpRequest} -- 
    """
    if request.method == 'GET':
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return JsonResponse(serializer.data, safe=False)
