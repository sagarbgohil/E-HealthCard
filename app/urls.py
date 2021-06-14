from . import views
from django.urls import path

urlpatterns = [
    path('', views.home_page, name="home"),
    path('login/', views.login_page, name="login"),
    path('register/', views.register_page, name="register"),
    path('patient/', views.patient_page, name="patient"),
    path('logout/', views.logout, name="logout"),
    path('doctor/', views.doctor_page, name="doctor"),
    path('paramedics/', views.paramedics_page, name="paramedics"),
    path('registerdoctor/', views.register_doctor, name="registerdoctor"),
    path('registerparamedics/', views.register_paramedics, name="registerparamedics"),
    path('getpatientinfo/', views.get_patient_data, name="getpatientinfo"),
    path('getpatientinfoparamedics/', views.get_patient_data_paramedics, name="getpatientinfoparamedics"),
    path('gethealthinfo/', views.get_health_info, name="gethealthinfo"),
    path('getfiledata/', views.get_file_data, name="getfiledata"),
    path('addhealthdata/', views.add_health_info, name="addhealthdata"),
    path('addfiledata/', views.add_file_info, name="addfiledata"),
    path('editpatientdata/', views.edit_patient_data, name="editpatientdata"),
    path('forgetpassword/', views.forget_password, name='forgetpassword'),
    path('resetpassword/', views.reset_password, name='resetpassword'),
]