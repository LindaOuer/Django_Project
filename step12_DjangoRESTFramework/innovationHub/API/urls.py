from django.urls import path
from . import views

urlpatterns = [
    path('students/', views.students_List),
    path('students/<int:pk>/', views.student_detail),
]
