from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from .models import *
from django.db.models import *
from datetime import date
from django.http import HttpResponse
from django.template import loader

# Create your views here.
def login_page(request):

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
                return patient_page(request)
            else:
                error = "Password is wrong"
    
        except Patient.DoesNotExist as e:
            error = "Email id is wrong"

    context = {
        "title": "Login",
        "error": error
    }
    return render(request, 'app/login_page.html', context)

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
                email_id =register_data.get("email_id"),
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
            return redirect('/login/', request=request)
            # return render(request, 'app/login_page.html')

    except Exception as e:
        pass

    context = {
        "title": "Register"
    }
    return render(request, 'app/registration_page.html', context)

def home_page(request):

    context = {
        "title" : "Home"
    }
    return render(request, 'app/home_page.html')

def patient_page(request):

    mail = request.session['emailid']
    data = Patient.objects.get(email_id = mail)

    # if request.POST:
    #     login_data = request.POST.dict()
    #     mail = login_data.get("email_id")
    #     password = login_data.get("password")
    #     try:
    #         data = Patient.objects.get(email_id = mail)
    #         if check_password(password, data.password):
    #             # return patient_page(request, data)
    #             pass
    #         else:
    #             error = "Password is wrong"
    #             context = {
    #                 "title": "Login",
    #                 "error": error
    #             }
    #             return render(request, 'app/login_page.html', context)
    
    #     except Patient.DoesNotExist as e:
    #         error = "Email id is wrong"
    #         context = {
    #                 "title": "Login",
    #                 "error": error
    #             }
    #         return render(request, 'app/login_page.html', context)

    phone_number = PhoneNumber.objects.get(patient_id = data)
    add = data.address_1 + ", "  + data.city + ", "  + data.state + ", "  + data.country + ", " +  str(data.pincode)
    doctor_data = ""
    paramedics_data = ""
    try:
        doctor_data = Doctor.objects.get(patient_id = data)
        paramedics_data = Paramedics.objects.get(patient_id = data)            
    except Doctor.DoesNotExist as e:
        print("Not doctor")
    except Paramedics.DoesNotExist as e:
        print("Not paramedics")
    if doctor_data:
        context = {
            "title": "Patient",
            "patient": data,
            "add": add,
            "phone_number": phone_number,
            "doctor": "yes"
        }
    elif paramedics_data:
        context = {
            "title": "Patient",
            "patient": data,
            "add": add,
            "phone_number": phone_number,
            "paramedics": "yes"
        }
    else:
        context = {
            "title": "Patient",
            "patient": data,
            "add": add,
            "phone_number": phone_number,
            "patient_check": "yes"
        }
    
    template = loader.get_template('app/patient_page.html')
    response = HttpResponse(template.render(context, request))
    response['Location'] = "patient/"
    return response
    # return render(request, 'app/patient_page.html', context)

def doctor_page(request):
    register_data = request.POST.dict()
    name = register_data.get("name")
    patient_id = register_data.get("patient_id")

    context = {
        "title": "Doctor",
        "name": name,
        "patient_id": patient_id
    }
    return render(request, 'app/doctor_page.html', context)

def get_patient_data(request):
    if(request.POST):
        register_data = request.POST.dict()
        mail = register_data.get("email_id")
        try:
            data = Patient.objects.get(email_id = mail)
            context= {
                "data": data,
                "patient_id": register_data.get("patient_id"),
                "name": register_data.get("name")
            }
            return render(request, 'app/doctor_page.html', context)
                
        except Patient.DoesNotExist as e:
            print("error")
    return render(request, 'app/doctor_page.html')

def get_patient_data_paramedics(request):
    if(request.POST):
        register_data = request.POST.dict()
        mail = register_data.get("email_id")
        try:
            patient = Patient.objects.get(email_id = mail)
            filedata = HealthInfo.objects.get(patient_id = patient)
            context = {
                "data": filedata,
                "patient_id": register_data.get("patient_id"),
                "name": register_data.get("name"),
                "patient_name": patient.name
            }
            return render(request, 'app/peramedics_page.html', context)
                
        except Patient.DoesNotExist as e:
            print("error")
    return render(request, 'app/peramedics_page.html')

def register_doctor(request):
    if request.POST:
        register_data  = request.POST.dict()

        max_id = Doctor.objects.all().aggregate(Max('doctor_id'))['doctor_id__max']
        print(max_id)
        max_id = int(max_id) if max_id is not None else 0
        max_id += 1 
        max_id = str(max_id).zfill(10) if max_id is not None else 1
        
        # combine data into fullname
        patient_id = register_data.get("patient_id")
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
        return patient_page(request, patient)
    return render(request, 'app/doctor_register.html')

def register_paramedics(request):
    if request.POST:
        register_data  = request.POST.dict()

        max_id = Paramedics.objects.all().aggregate(Max('paramedics_id'))['paramedics_id__max']
        max_id = int(max_id) if max_id is not None else 0
        max_id += 1 
        max_id = str(max_id).zfill(10) if max_id is not None else 1
        
        # combine data into fullname
        patient_id = register_data.get("patient_id")

        patient = Patient.objects.get(patient_id = patient_id)
        license_id = register_data.get("licence_id")

        # Adding record into Patient table
        record, _ = Paramedics.objects.update_or_create(paramedics_id = max_id,
            patient_id = patient,
            vehicle_licence_num = license_id
            )
        return patient_page(request, patient)
        # return render(request, 'app/patient_page.html', patient)

    return render(request, 'app/peramedics_register.html')

def get_health_info(request):

    if request.POST:

        register_data  = request.POST.dict()

        try:
            patient_id = register_data.get("patient_id")
            patient = Patient.objects.get(patient_id = patient_id)
            data = HealthInfo.objects.get(patient_id = patient)

            context = {
                "data": data
            }

            return render(request, 'app/health_info_page.html', context)

        except (Patient.DoesNotExist, HealthInfo.DoesNotExist) as a:
            pass

    return render(request, 'app/health_info_page.html')

def get_file_data(request):
    if request.POST:

        register_data  = request.POST.dict()

        try:
            patient_id = register_data.get("patient_id")
            patient = Patient.objects.get(patient_id = patient_id)
            data = File.objects.get(patient_id = patient)

            context = {
                "data": data
            }

            return render(request, 'app/file_info_page.html', context)

        except (Patient.DoesNotExist, File.DoesNotExist) as a:
            pass

    return render(request, 'app/file_info_page.html')

def add_health_info(request):

    if request.POST:
        register_data = request.POST.dict()

        max_id = HealthInfo.objects.all().aggregate(Max('health_id'))['health_id__max']
        max_id = int(max_id) if max_id is not None else 0
        max_id += 1 
        max_id = str(max_id).zfill(10) if max_id is not None else 1

        patient_id = register_data.get('patient_id')
        height = register_data.get('height')
        weight = register_data.get('weigth')
        blood_grp = register_data.get('blood_grp')
        emergency_number = register_data.get('emergency_number')
        medication = register_data.get("medication")

        patient = Patient.objects.get(patient_id = patient_id)
           
        record, _ = HealthInfo.objects.update_or_create(
            health_id = max_id,
            patient_id = patient,
            height = height,
            weight = weight,
            blood_grp = blood_grp,
            emergency_number = emergency_number,
            medication = medication
        )

        return redirect('/gethealthinfo/', request=request)

    return render(request, 'app/health_info_page.html')

def add_file_info(request):
    register_data = request.POST.dict()

    if request.POST:

        max_id = File.objects.all().aggregate(Max('file_id'))['file_id__max']
        max_id = int(max_id) if max_id is not None else 0
        max_id += 1 
        max_id = str(max_id).zfill(10) if max_id is not None else 1

        patient_id = register_data.get('patient_id')
        symptoms = register_data.get('symptom')
        diagnosis = register_data.get('diagnosis')
        prescribed_medicine = register_data.get('prescribedMedicine')
        notes = register_data.get('note')
        created_date = date.today()
        doctor_id = register_data.get('doctor_patient_id')
        print(doctor_id)
        
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
        
    name = register_data.get("name")
    patient_id = register_data.get("patient_id")
    context = {
        "title": "Paramedics",
        "name": name,
        "patient_id": patient_id
    }

    return render(request, 'app/doctor_page.html', context)

def paramedics_page(request):
    register_data = request.POST.dict()
    name = register_data.get("name")
    patient_id = register_data.get("patient_id")

    context = {
        "title": "Paramedics",
        "name": name,
        "patient_id": patient_id
    }

    return render(request, 'app/peramedics_page.html', context)

