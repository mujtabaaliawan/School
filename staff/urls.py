from django.urls import path
from staff import views


urlpatterns = [
    path('staff', views.AdminList.as_view(), name='staff_list'),
    path('staff/new', views.AdminCreate.as_view(), name='new_staff'),
    path('staff/<int:pk>', views.AdminUpdate.as_view(), name='staff_update'),
]