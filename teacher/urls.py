from django.urls import path
from teacher import views


urlpatterns = [
    path('faculty', views.TeacherList.as_view(), name='faculty_list'),
    path('faculty/detail', views.TeacherDetailList.as_view(), name='faculty_detail'),
    path('faculty/new', views.TeacherCreate.as_view(), name='new_faculty'),
    path('faculty/<int:pk>', views.TeacherUpdate.as_view(), name='faculty_update'),
]
