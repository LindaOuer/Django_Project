from django.urls import path
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register('projects', views.ProjectViewSet, basename='projects')
urlpatterns = router.urls
