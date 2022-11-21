from django.urls import path
from result import views


urlpatterns = [
    path('result', views.ResultList.as_view(), name='result_list'),
    path('result/new', views.ResultCreate.as_view(), name='result_new'),
    path('result/<int:pk>', views.ResultUpdate.as_view(), name='result_update'),
]