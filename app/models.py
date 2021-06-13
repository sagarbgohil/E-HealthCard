from django.db import models

# Create your models here.
class Patient(models.Model):
    patient_id = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=20)
    email_id = models.CharField(max_length=20)
    birth_date = models.DateField()
    adhaar_number = models.BigIntegerField()
    permission = models.BigIntegerField()
    gender = models.CharField(max_length=10)
    age = models.CharField(max_length=5)
    address_1 = models.CharField(max_length=50)
    city = models.CharField(max_length=10)
    state = models.CharField(max_length=10)
    country = models.CharField(max_length=10)
    pincode = models.BigIntegerField()
    password = models.CharField(max_length=200)
    def __str__(self):
        return str(self.patient_id)

class PhoneNumber(models.Model):
    phone_number_id = models.CharField(max_length=10, primary_key=True)
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    phone_number = models.BigIntegerField()
    def __str__(self):
        return str(self.phone_number_id)

class Doctor(models.Model):
    doctor_id = models.CharField(primary_key=True, max_length=10)
    patient_id = models.OneToOneField(Patient, on_delete=models.CASCADE, default="")
    hospital_name = models.CharField(max_length=20, default="")
    designation = models.CharField(max_length=15, default="")
    licence_id = models.CharField(max_length=20, default="")    
    def __str__(self):
        return str(self.doctor_id)

class File(models.Model):
    file_id = models.CharField(primary_key=True, max_length=10)
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    symptoms = models.CharField(max_length=20)
    diagnosis = models.CharField(max_length=20)
    prescribed_medicine = models.CharField(max_length=30)
    notes = models.CharField(max_length=30)
    created_date = models.DateField()
    def __str__(self):
        return str(self.file_id)

class HealthInfo(models.Model):
    health_id = models.CharField(primary_key=True, max_length=10)
    patient_id = models.OneToOneField(Patient, on_delete=models.CASCADE)
    height = models.BigIntegerField()
    weight = models.BigIntegerField()
    blood_grp = models.CharField(max_length=5)
    emergency_num = models.BigIntegerField()
    medication = models.CharField(max_length=30)
    def __str__(self):
        return str(self.health_id)

class Allergies(models.Model):
    allergies_id = models.CharField(primary_key=True, max_length=10)
    health_id = models.ForeignKey(HealthInfo, on_delete=models.CASCADE)
    allergies = models.CharField(max_length=30)
    def __str__(self):
        return str(self.allergies_id)

class Paramedics(models.Model):
    paramedics_id = models.CharField(primary_key=True, max_length=10)
    patient_id = models.OneToOneField(Patient, on_delete=models.CASCADE)
    vehicle_licence_num = models.BigIntegerField()
    def __str__(self):
        return str(self.paramedics_id)

class Metadata(models.Model):
    meta_data_id = models.CharField(primary_key=True, max_length=10)
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    created_date = models.DateField()
    last_modify_date = models.DateField()
    last_login_date = models.DateField()
    verified_date = models.DateField()
    def __str__(self):
        return str(self.meta_data_id)

class Admin(models.Model):
    admin_id = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=20)
    organization = models.CharField(max_length=20)
    def __str__(self):
        return str(self.admin_id)

class VerifiedBy(models.Model):
    verified_by_id = models.CharField(primary_key=True, max_length=10)
    admin_id = models.ForeignKey(Admin, on_delete=models.CASCADE)
    doctor_id = models.OneToOneField(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    def __str__(self):
        return str(self.admin_id)
