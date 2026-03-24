
# Create your views here.
from django.shortcuts import render

def home_view(request):
    return render(request, 'stats_app/index.html')
