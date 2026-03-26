from django.urls import path
from . import views

app_name = "f1_app"   # <-- дуже важливо, щоб {% url 'f1_app:dashboard' %} працював

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
]
