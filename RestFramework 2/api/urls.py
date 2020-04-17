from django.urls import path
from . import views

urlpatterns = [
    path('projects/', views.projects_List),
    path('projects/<int:pk>/', views.project_detail),
]
