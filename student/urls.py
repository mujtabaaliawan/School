from django.urls import path
from student import views

urlpatterns = [
    path('student', views.StudentList.as_view(), name='student_list'),
    path('student/new', views.StudentCreate.as_view(), name='student_new'),
    path('student/<int:pk>', views.StudentUpdate.as_view(), name='student_update'),
    path('enrollment/<int:pk>', views.EnrollmentUpdate.as_view(), name='enrollment'),
]
