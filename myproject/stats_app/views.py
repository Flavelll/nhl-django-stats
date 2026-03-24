
# Create your views here.
from django.shortcuts import render

def home_view(request):
    # Вказуємо повний шлях з урахуванням підпапки
    return render(request, 'stats_app/index.html')
