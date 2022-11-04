from django.urls import path
from teacher import views


urlpatterns = [
    path('teacher/', views.TeacherViewSet.as_view()),
]
