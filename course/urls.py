from django.urls import path
from course import views


urlpatterns = [
    path('course', views.CourseList.as_view(), name='course_list'),
    path('course/new', views.CourseCreate.as_view(), name='course_new'),
    path('course/<int:pk>', views.CourseUpdate.as_view(), name='course_update'),
]
