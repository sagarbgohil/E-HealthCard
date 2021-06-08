from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
def login_page(request):
    context = {
        "title": "Login"
    }
    return render(request, 'app/login_page.html', context)

def register_page(request):
    context = {
        "title": "Register"
    }
    return render(request, 'app/registration_page.html', context)

def home_page(request):
    context = {
        "title" : "Home"
    }
    return render(request, 'app/home_page.html', context)
