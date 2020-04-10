from django.urls import path
from .views import projectDetails, index, listProjects, project_ListView, project_DetailView, project_CreateView, \
    deleteProjects, project_UpdateView, add_student, student_ListView

urlpatterns = [
    path('', index, name='home'),
    # Projects
    path('projects/', listProjects, name="project_list"),
    path('projects/<int:pId>/', projectDetails, name='project_details'),
    path('projects/list', project_ListView.as_view(), name="projectsLV"),
    path('projects/details/<int:pk>/',
         project_DetailView.as_view(), name='projectDV'),
    path('projects/delete/<int:pId>/', deleteProjects, name='project_delete'),
    path('projects/new/', project_CreateView.as_view(), name='project_New'),
    path('projectsDV/update/<int:pk>/',
         project_UpdateView.as_view(), name='projectUpV'),

    # Students
    path('students/create/', add_student, name='Student_New'),
    path('students/', student_ListView.as_view(), name="studentsLV"),
]
