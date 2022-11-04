from django.urls import path
from student import views

urlpatterns = [
    path('student_register/', views.StudentViewSet.as_view()),
    path('student_enroll/<int:pk>', views.EnrollCourseViewSet.as_view()),
]