
# stats_app/urls.py
from django.urls import path
from . import views

app_name = 'stats_app'

urlpatterns = [
    path('', views.home_view, name='index'),
]
