from django.shortcuts import render

# Create your views here.
def login_page(request):
    context = {
        "title": "Login"
    }
    return render(request, 'eCard/login_page.html', context)

def register_page(request):
    context = {
        "title": "Register"
    }
    return render(request, 'eCard/registration_page.html', context)

def loder(request):
    return render(request, 'eCard/loder.html')

def home_page(request):
    context = {
        "title" : "Home"
    }
    return render(request, 'eCard/home_page.html', context)
