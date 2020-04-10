from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from django.urls import reverse
from django.views.generic import ListView, DetailView, UpdateView, CreateView

from .forms import AddStudentForm, CreateUserForm
from .models import Project, Student


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)

                return redirect('login')

        context = {'form': form}
        return render(request, 'hub/register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'hub/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def index(request):
    return render(request, 'hub/index.html')


@login_required(login_url='login')
def listProjects(request):
    project_list = Project.objects.all()
    return render(request, 'hub/listProjects.html', {'project_list': project_list})


@login_required(login_url='login')
def projectDetails(request, pId):
    project = get_object_or_404(Project, pk=pId)
    return render(request, 'hub/project_details.html', {'project': project})


@method_decorator(login_required, name='dispatch')
class project_ListView(ListView):
    model = Project
    template_name = 'hub/project_ListView.html'
    context_object_name = 'projects'
    fields = "__all__"
    ordering = ['-updated_at']


@method_decorator(login_required, name='dispatch')
class project_DetailView(DetailView):
    model = Project
    context_object_name = 'project'


@method_decorator(login_required, name='dispatch')
class project_UpdateView(UpdateView):
    model = Project
    fields = ['projectName',
              'projectDuration',
              'timeAllocated',
              'needs',
              'description', 'creator']


@method_decorator(login_required, name='dispatch')
class project_CreateView(CreateView):
    model = Project
    fields = ['projectName',
              'projectDuration',
              'timeAllocated',
              'needs',
              'description', 'creator']


@method_decorator(login_required, name='dispatch')
def deleteProjects(request, pId):
    project = get_object_or_404(Project, pk=pId)
    project.delete()
    return HttpResponseRedirect(reverse('projectsLV'))


@method_decorator(login_required, name='dispatch')
class student_ListView(ListView):
    model = Student
    template_name = 'innovApp/student_List.html'
    context_object_name = 'students'


@login_required(login_url='login')
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
