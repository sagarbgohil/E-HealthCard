from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.hashers import make_password, check_password
from .models import *

# Create your views here.
def login_page(request):

    if(request.POST):
        login_data = request.POST.dict()
        mail = login_data.get("email_id")
        password = login_data.get("password")

        try:
            data = Patient.objects.get(email_id = mail)
        except Patient.DoesNotExist as e:
            print("error")
        
        print("Data: ", data)
        if check_password(password, data.password):
            print("success")
        else:
            print('Error')
        # print(email_id, password)

        return render(request, 'app/home_page.html')

    context = {
        "title": "Login"
    }
    return render(request, 'app/login_page.html', context)

def register_page(request):
    if request.POST:
        register_data  = request.POST.dict()

        fname = register_data.get("fname")
        mname = register_data.get("mname")
        lname = register_data.get("lname")
        mail = register_data.get("email_id")
        bdate = register_data.get("bdate")
        adhaar = register_data.get("adhaar")
        phone = register_data.get("phone")
        gender = register_data.get("gender")
        add = register_data.get("add")
        city = register_data.get("city")
        state = register_data.get("state")
        country = register_data.get("country")
        pincode = register_data.get("pincode")
        password = register_data.get("password")

        fullname = fname + " " + mname + " " + lname

        record = Patient.objects.update_or_create(name = fullname,
            email_id = mail,
            birth_date = bdate,
            adhaar_number = adhaar,
            gender = gender,
            address_1 = add,
            city = city,
            state = state,
            country = country,
            pincode = pincode,
            password = make_password(password),
            permission = 1)

        # record.save()
        # print(fname, mname, lname, mail, bdate, adhaar, phone, gender, add, city, state, country, pincode, password, cpassword)


        return render(request, 'app/home_page.html')
    context = {
        "title": "Register"
    }
    return render(request, 'app/registration_page.html', context)

def home_page(request):

    context = {
        "title" : "Home"
    }
    return render(request, 'app/home_page.html')
