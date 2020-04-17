from django.urls import path
from . import views

urlpatterns = [
    path('projects/', views.projects_List.as_view()),
    path('projects/<int:pk>/', views.project_detail.as_view()),
]
