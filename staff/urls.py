from django.urls import path
from staff import views


urlpatterns = [
    path('staff', views.StaffList.as_view(), name='staff_list'),
    path('staff/new', views.StaffCreate.as_view(), name='staff_new'),
    path('staff/<int:pk>', views.StaffUpdate.as_view(), name='staff_update'),
]