from django.urls import path
from student import views

urlpatterns = [
    path('student', views.StudentList.as_view(), name='student'),
    path('student/new', views.StudentCreate.as_view(), name='student_new'),
    path('student/<int:pk>', views.StudentUpdate.as_view(), name='student_update'),
    path('enrollment/<int:pk>', views.EnrollmentNew.as_view(), name='enrollment'),
    path('enrollment/<int:pk>/update', views.EnrollmentUpdate.as_view(), name='enrollment_update'),
]
