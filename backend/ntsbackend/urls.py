from django.urls import path

from .views import get_name

urlpatterns = [
    path('', get_name, name='home'),
]