from django.urls import path
from .views import ResultViewSet

print("hello")

urlpatterns = [
    path('result/', ResultViewSet.as_view()),
]
