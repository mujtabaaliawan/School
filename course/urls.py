from django.urls import path
from course import views


urlpatterns = [
    path('subject', views.CourseList.as_view(), name='course'),
    path('subject/new', views.CourseCreate.as_view(), name='new_course'),
    path('subject/<int:pk>/update', views.CourseUpdate.as_view(), name='course_update'),
]
