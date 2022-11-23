from django.urls import path
from teacher import views


urlpatterns = [
    path('teacher', views.TeacherList.as_view(), name='teacher_list'),
    path('teacher/new', views.TeacherCreate.as_view(), name='teacher_new'),
    path('teacher/<int:pk>', views.TeacherRetrieveUpdate.as_view(), name='teacher_update'),
]
