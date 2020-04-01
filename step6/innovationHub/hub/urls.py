from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('projects/', views.listProjects, name="project_list"),
    path('projects/<int:pId>/', views.projectDetails, name='project_details'),
]
