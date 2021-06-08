from . import views
from django.urls import path

urlpatterns = [
    path('', views.home_page, name="home"),
    path('login/', views.login_page, name="login"),
    path('register/', views.register_page, name="register")
]