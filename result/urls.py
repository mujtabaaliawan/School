from django.urls import path
from .views import Result


urlpatterns = [
    path('result/', Result.as_view(), name='result_section'),
]