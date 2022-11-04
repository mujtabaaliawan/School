from django.urls import path
from .views import CourseViewSet


urlpatterns = [
    path('course/', CourseViewSet.as_view()),
]