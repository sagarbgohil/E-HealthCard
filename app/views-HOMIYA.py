from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
def login_page(request):
    
    if(request.POST):
        login_data = request.POST.dict()
        email_id = login_data.get("email_id")
        password = login_data.get("password")
        
        print(email_id, password)

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
        email_id = register_data.get("email_id")
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
        cpassword = register_data.get("cpassword")

        name = fname + mname + lname

        print(fname, mname, lname, email_id, bdate, adhaar, phone, gender, add, city, state, country, pincode, password, cpassword)

        return render(request, 'app/home_page.html')
    context = {
        "title": "Register"
    }
    return render(request, 'app/registration_page.html', context)

def home_page(request):

    context = {
        "title" : "Home"
    }
    return render(request, 'app/home_page.html', context)
