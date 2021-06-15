from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from .models import *
from django.db.models import *
from datetime import date
from django.http import HttpResponse
from django.template import loader
from django.core.mail import send_mail

def login_page(request):

    success = ""
    if 'success_pwd' in request.session:
        success = request.session['success_pwd']
    print(success)
    error = ""
    if(request.POST):
        login_data = request.POST.dict()
        mail = login_data.get("email_id")
        print(mail)
        password = login_data.get("password")
        try:
            data = Patient.objects.get(email_id = mail)
            if check_password(password, data.password):
                request.session['emailid'] = str(mail)
                # return patient_page(request)
                request.session.set_expiry(600)
                return redirect('/patient/', request=request)
            else:
                error = "Password is wrong"
    
        except Patient.DoesNotExist as e:
            error = "Email id is wrong"

    return render(request, 'app/login_page.html', {"error": error, "success": success})

def logout(request):
    request.session.flush()
    return redirect('/')

def register_page(request):
    try:
        if request.POST:
            register_data  = request.POST.dict()

            # combine data into fullname
            fname = register_data.get("fname")
            mname = register_data.get("mname")
            lname = register_data.get("lname")
            fullname = str(fname) + " " + str(mname) + " " + str(lname)
            
            # Finding age 
            bdate = register_data.get("bdate")
            today = date.today()
            age = ""
            dob = date(int(bdate[:4]), int(bdate[5:7]), int(bdate[8:10]))
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

            # Generating patient id
            max_id = Patient.objects.all().aggregate(Max('patient_id'))['patient_id__max']
            max_id = int(max_id) if max_id is not None else 0
            max_id += 1
            max_id = str(max_id).zfill(10) if max_id is not None else 1
            
            # Adding record into Patient table
            record, _ = Patient.objects.update_or_create(name = fullname,
                patient_id = max_id,
                email_id = register_data.get("email_id"),
                birth_date = bdate,
                adhaar_number = register_data.get("adhaar"),
                gender = register_data.get("gender"),
                address_1 = register_data.get("add"),
                city = register_data.get("city"),
                state = register_data.get("state"),
                country = register_data.get("country"),
                pincode = register_data.get("pincode"),
                age = age,
                password = make_password(register_data.get("password")),
                permission = 1)

            # Adding record phone number in PhoneNumber table
            phone_id = PhoneNumber.objects.all().aggregate(Max('phone_number_id'))['phone_number_id__max']
            phone_id = int(phone_id) if phone_id is not None else 0
            phone_id += 1
            phone_id = str(phone_id).zfill(10) if phone_id is not None else 1
            phone_record = PhoneNumber.objects.update_or_create(
                phone_number_id = phone_id,
                patient_id = record,
                phone_number = register_data.get("phone")
            )
            request.session['emailid'] = register_data.get("email_id")
            return redirect('/patient/', request=request)
            # return render(request, 'app/login_page.html')

    except Exception as e:
        print(e)

    return render(request, 'app/registration_page.html')

def home_page(request):
    if 'emailid' in request.session:
        return redirect('/patient/', request=request)
    return render(request, 'app/home_page.html')

def patient_page(request):

    if 'emailid' not in request.session:
        return redirect('/login/')
    mail = request.session['emailid']
    data = Patient.objects.get(email_id = mail)

    phone_number = PhoneNumber.objects.get(patient_id = data)
    add = data.address_1 + ", "  + data.city + ", "  + data.state + ", "  + data.country + ", " +  str(data.pincode)
    doctor_data = None
    paramedics_data = None

    try:
        doctor_data = Doctor.objects.get(patient_id = data)
    except Doctor.DoesNotExist as e:
        print("Not doctor")

    try:
        paramedics_data = Paramedics.objects.get(patient_id = data)            
    except Paramedics.DoesNotExist as e:
        print("Not paramedics")

    if doctor_data:
        request.session['doctor'] = 'yes'
        print('doctor')
    elif paramedics_data:
        request.session['paramedics'] = 'yes'
        print("paramedics")
    else:
        request.session['patient_check'] = 'yes'
        print("patient")

    request.session['patient'] = data
    request.session['add'] = add
    request.session['phone_number'] = phone_number

    return render(request, 'app/patient_page.html')

def doctor_page(request):
    if 'emailid' not in request.session:
        return redirect('/login/')

    # register_data = request.POST.dict()
    # request.session['doctorname'] = register_data.get("name")
    # request.session['doctorid'] = register_data.get("patient_id")

    request.session['doctorname'] = request.session['patient'].name
    request.session['doctorid'] = request.session['patient'].patient_id

    # context = {
    #     "title": "Doctor",
    #     "name": name,
    #     "patient_id": patient_id
    # }
    return render(request, 'app/doctor_page.html')

def paramedics_page(request):
    if 'emailid' not in request.session:
        return redirect('/login/')

    # register_data = request.POST.dict()
    # request.session['doctorname'] = register_data.get("name")
    # request.session['doctorid'] = register_data.get("patient_id")

    request.session['paramedicname'] = request.session['patient'].name
    request.session['paramedicid'] = request.session['patient'].patient_id

    # context = {
    #     "title": "Doctor",
    #     "name": name,
    #     "patient_id": patient_id
    # }
    return render(request, 'app/peramedics_page.html')

    # register_data = request.POST.dict()
    # name = register_data.get("name")
    # patient_id = register_data.get("patient_id")

    # context = {
    #     "title": "Paramedics",
    #     "name": name,
    #     "patient_id": patient_id
    # }

    # return render(request, 'app/peramedics_page.html', context)

def get_patient_data(request):
    if(request.POST):
        register_data = request.POST.dict()
        mail = register_data.get("email_id")
        try:
            data = Patient.objects.get(email_id = mail)
            health_info = HealthInfo.objects.get(patient_id = data)
            request.session["data"] = data
            request.session["health"] = health_info
            if "error" in request.session:
                del request.session['error']
            # context= {
            #     "data": data,
            #     "patient_id": register_data.get("patient_id"),
            #     "name": register_data.get("name")
            # }

            # return render(request, 'app/doctor_page.html')
                
        except (Patient.DoesNotExist, HealthInfo.DoesNotExist) as e:
            print("error")
            request.session['error'] = "Data not found"

    return redirect('/doctor/') 
    # return render(request, 'app/doctor_page.html')

def get_patient_data_paramedics(request):
    if(request.POST):
        register_data = request.POST.dict()
        mail = register_data.get("email_id")
        try:
            data = Patient.objects.get(email_id = mail)
            health_info = HealthInfo.objects.get(patient_id = data)
            request.session["data"] = data
            request.session["health"] = health_info
            del request.session['error']
        except (Patient.DoesNotExist, HealthInfo.DoesNotExist) as e:
            print("error")
            request.session['error'] = "Data not found"
            
    return redirect('/paramedics/') 
    
    # if(request.POST):
    #     register_data = request.POST.dict()
    #     mail = register_data.get("email_id")
    #     try:
    #         patient = Patient.objects.get(email_id = mail)
    #         filedata = HealthInfo.objects.get(patient_id = patient)
    #         context = {
    #             "data": filedata,
    #             "patient_id": register_data.get("patient_id"),
    #             "name": register_data.get("name"),
    #             "patient_name": patient.name
    #         }
    #         return render(request, 'app/peramedics_page.html', context)
                
    #     except Patient.DoesNotExist as e:
    #         print("error")
    # return render(request, 'app/peramedics_page.html')

def register_doctor(request):
    if request.POST:
        register_data  = request.POST.dict()

        max_id = Doctor.objects.all().aggregate(Max('doctor_id'))['doctor_id__max']
        print(max_id)
        max_id = int(max_id) if max_id is not None else 0
        max_id += 1 
        max_id = str(max_id).zfill(10) if max_id is not None else 1
        
        # combine data into fullname
        patient_id = request.session['patient'].patient_id
        hospital_name = register_data.get("hospital_name")
        designation = register_data.get("designation")
        licence_id = register_data.get("licence_id")
        
        patient = Patient.objects.get(patient_id = patient_id)

        # Adding record into Patient table
        record, _ = Doctor.objects.update_or_create(doctor_id = max_id,
            patient_id = patient,
            hospital_name = hospital_name,
            designation = designation,
            licence_id = licence_id)

        if 'patient_check' in request.session:
            del request.session['patient_check'] 

        return redirect('/patient')

    return render(request, 'app/doctor_register.html')

def register_paramedics(request):
    if request.POST:
        register_data  = request.POST.dict()

        max_id = Paramedics.objects.all().aggregate(Max('paramedics_id'))['paramedics_id__max']
        max_id = int(max_id) if max_id is not None else 0
        max_id += 1 
        max_id = str(max_id).zfill(10) if max_id is not None else 1
        
        # combine data into fullname
        patient_id = request.session['patient'].patient_id

        patient = Patient.objects.get(patient_id = patient_id)
        license_id = register_data.get("licence_id")

        # Adding record into Patient table
        record, _ = Paramedics.objects.update_or_create(paramedics_id = max_id,
            patient_id = patient,
            vehicle_licence_num = license_id
            )

        if 'patient_check' in request.session:
            del request.session['patient_check'] 

        return redirect('/patient')
        # return render(request, 'app/patient_page.html', patient)

    return render(request, 'app/peramedics_register.html')

def get_health_info(request):
    if 'emailid' not in request.session:
        return redirect('/login/')
    try:
        patient_id = request.session['patient'].patient_id
        patient = Patient.objects.get(patient_id = patient_id)
        data = HealthInfo.objects.get(patient_id = patient)
        request.session['healthinfo'] = data
    except (Patient.DoesNotExist, HealthInfo.DoesNotExist) as a:
        if 'healthinfo' in request.session:
            del request.session['healthinfo'] 
        print("no health data found")
        request.session['error'] = "no health data found"

    return render(request, 'app/health_info_page.html')

def get_file_data(request):
    if 'emailid' not in request.session:
            return redirect('/login/')

    try:
        patient_id = request.session['patient'].patient_id
        patient = Patient.objects.get(patient_id = patient_id)
        data = File.objects.filter(patient_id = patient)
        print(data)
        request.session['filedata'] = data

    except (Patient.DoesNotExist, File.DoesNotExist) as a:
        if 'filedata' in request.session:
            del request.session['filedata'] 
        print("no file data found")
        request.session['error'] = "no file data found"

    return render(request, 'app/file_info_page.html')

def add_health_info(request):
    if 'emailid' not in request.session:
        return redirect('/login/')
    if request.POST:
        register_data = request.POST.dict()

        max_id = HealthInfo.objects.all().aggregate(Max('health_id'))['health_id__max']
        max_id = int(max_id) if max_id is not None else 0
        max_id += 1 
        max_id = str(max_id).zfill(10) if max_id is not None else 1

        patient_id = request.session['patient'].patient_id
        height = register_data.get('height')
        weight = register_data.get('weight')
        blood_grp = register_data.get('blood_grp')
        emergency_number = register_data.get('emergency_num')
        medication = register_data.get("medication")

        if len(emergency_number) < 1 or len(emergency_number) > 10:
            request.session['errorfield'] = "Enter valid data"
            return redirect('/gethealthinfo/')

        if 'errorfield' in request.session:
            del request.session['errorfield']

        patient = Patient.objects.get(patient_id = patient_id)
           
        record, _ = HealthInfo.objects.update_or_create(
            health_id = max_id,
            patient_id = patient,
            height = height,
            weight = weight,
            blood_grp = blood_grp,
            emergency_num = emergency_number,
            medication = medication
        )
        data = HealthInfo.objects.get(patient_id = patient)
        request.session['healthinfo'] = data
        return redirect('/gethealthinfo/')

    return render(request, 'app/health_info_page.html')

def add_file_info(request):
    if 'emailid' not in request.session:
            return redirect('/login/')
    register_data = request.POST.dict()

    if request.POST:

        max_id = File.objects.all().aggregate(Max('file_id'))['file_id__max']
        max_id = int(max_id) if max_id is not None else 0
        max_id += 1 
        max_id = str(max_id).zfill(10) if max_id is not None else 1

        patient_id = request.session['data'].patient_id
        symptoms = register_data.get('symptom')
        diagnosis = register_data.get('diagnosis')
        prescribed_medicine = register_data.get('prescribedMedicine')
        notes = register_data.get('note')
        created_date = date.today()
        doctor_id = request.session['patient'].patient_id
        print(doctor_id)
        
        if len(symptoms) < 1 or len(diagnosis) < 1 or len(prescribed_medicine) < 1 or len(notes) < 1:
            request.session['errorfield'] = "enter valid input"
            return redirect('/doctor')

        if 'errorfield' in request.session:
            del request.session['errorfield']


        patient = Patient.objects.get(patient_id = patient_id)
        doctor = Doctor.objects.get(patient_id = doctor_id)

        record, _ = File.objects.update_or_create(
            file_id = max_id,
            patient_id = patient,
            doctor_id = doctor,
            symptoms = symptoms,
            diagnosis = diagnosis,
            prescribed_medicine = prescribed_medicine,
            notes = notes,
            created_date = created_date,
        )

    return redirect('/doctor')

def edit_patient_data(request):
    if 'emailid' not in request.session:
        return redirect('/login/')
    if request.POST:
        print("post")
        request_data = request.POST.dict()

        mail = request.session['emailid']
        data = Patient.objects.get(email_id = mail)
        
        if len(request_data.get('pincode')) < 1 or len(request_data.get('phonenum')) != 10 or len(request_data.get('pincode')) > 6:
            request.session['errorfield'] = "enter valid input"
            return redirect('/editpatientdata/')

        if 'errorfield' in request.session:
            del request.session['errorfield']

        phone_data = PhoneNumber.objects.get(patient_id = data)
        phone = request_data.get('phonenum')
        phone_data.phone_number = phone
        phone_data.save()


        data.address_1 = request_data.get('add')
        data.city = request_data.get('city')
        data.state = request_data.get('state')
        data.country = request_data.get('country')
        data.pincode = request_data.get('pincode')

        data.save()        
        request.session['patient'] = data
        request.session['phone_number'] = phone_data

        request.session['emailid'] = data.email_id
        return redirect('/patient/')

    return render(request, 'app/edit_patient_data.html')

def forget_password(request):

    error = ""
    success = ""
    if request.POST:
        forget_data = request.POST.dict()
        mail = forget_data.get('email_id')
        data_mail = ""
        try:
            data = Patient.objects.get(email_id = mail)
            data_mail = data.email_id
        except Patient.DoesNotExist as e:
            error = "Email id is wrong"
        
        # msg = "Click below link to reset password"+"\n\n"+"http://127.0.0.1:8000/resetpassword/"

        
        if mail == data_mail:
            success = "Link has been send"
            
            # replace this two line with send mail logic
            # send_mail(
            #     'Reset Password',
            #     msg,
            #     'dig786335@gmail.com',
            #     [mail],
            #     fail_silently=False,
            # )

            request.session['emailid'] = str(mail)
            return redirect('/resetpassword/', request=request)

    return render(request, 'app/forget_password.html', {"error": error, "success": success})

def reset_password(request):

    if 'emailid' not in request.session:
        return redirect('/login/')

    mail = request.session['emailid']
    # print(mail)

    if request.POST:
        reset_password = request.POST.dict()
        new_passsword = reset_password.get('password')
        print(new_passsword)
        data = Patient.objects.get(email_id = mail)

        data.password = make_password(new_passsword)
        data.save()
        
        request.session['success_pwd'] = "Password Reset Successfully"
        
        return redirect('/login/', request=request)


    return render(request, 'app/reset_password.html')

