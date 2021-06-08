from django.urls import path
from . import views

urlpatterns = [
    path('', views.loder, name="loader"),
    path('home/', views.home_page, name="home"), 
    path('login/', views.login_page, name="login"),
    path('register/', views.register_page, name="register")
]
