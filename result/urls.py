from django.urls import path
from .views import ResultViewSet


urlpatterns = [
    path('result/', ResultViewSet.as_view()),
]