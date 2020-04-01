from django.shortcuts import render, get_object_or_404

# Create your views here.
from .models import Project


def index(request):
    return render(request, 'hub/index.html')


def listProjects(request):
    project_list = Project.objects.all()
    return render(request, 'hub/listProjects.html', {'project_list': project_list})


def projectDetails(request, pId):
    project = get_object_or_404(Project, pk=pId)
    return render(request, 'hub/project_details.html', {'project': project})
