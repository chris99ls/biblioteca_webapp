from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'webapp/index.html', {})


def login(request):
    return render(request, 'webapp/login.html', {})