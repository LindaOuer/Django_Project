from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse
from django.views.generic import ListView, DetailView, UpdateView, CreateView

from .forms import AddStudentForm
from .models import Project, Student


def index(request):
    return render(request, 'hub/index.html')


def listProjects(request):
    project_list = Project.objects.all()
    return render(request, 'hub/listProjects.html', {'project_list': project_list})


def projectDetails(request, pId):
    project = get_object_or_404(Project, pk=pId)
    return render(request, 'hub/project_details.html', {'project': project})


class project_ListView(ListView):
    model = Project
    template_name = 'hub/project_ListView.html'
    context_object_name = 'projects'
    fields = "__all__"
    ordering = ['-updated_at']


class project_DetailView(DetailView):
    model = Project
    context_object_name = 'project'


class project_UpdateView(UpdateView):
    model = Project
    fields = ['projectName',
              'projectDuration',
              'timeAllocated',
              'needs',
              'description', 'creator']


class project_CreateView(CreateView):
    model = Project
    fields = ['projectName',
              'projectDuration',
              'timeAllocated',
              'needs',
              'description', 'creator']


def deleteProjects(request, pId):
    project = get_object_or_404(Project, pk=pId)
    project.delete()
    return HttpResponseRedirect(reverse('projectsLV'))


class student_ListView(ListView):
    model = Student
    template_name = 'innovApp/student_List.html'
    context_object_name = 'students'


def add_student(request):
    if request.method == "GET":
        form = AddStudentForm()
        return render(request, 'hub/student_add.html', {'form': form})
    if request.method == "POST":
        form = AddStudentForm(request.POST)
        if form.is_valid():
            postStudent = form.save(commit=False)
            postStudent.save()
            return HttpResponseRedirect(reverse('studentsLV'))
        else:
            return render(request, 'hub/student_add.html',
                          {'msg_error': "Error when adding a student",
                           'form': form})
