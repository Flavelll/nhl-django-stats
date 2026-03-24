 
from django.urls import path
from . import views

app_name = 'nhl_app'

urlpatterns = [
    path('', views.nhl_stats_view, name='index'),
    path("agg/", views.nhl_agg_view, name="nhl_agg_view"),
]
