from django.urls import path
from result import views


urlpatterns = [
    path('results', views.ResultList.as_view(), name='result_list'),
    path('results/new', views.ResultCreate.as_view(), name='result_new'),
    path('results/<int:pk>', views.ResultUpdate.as_view(), name='result_update'),
]