from django.db import models

# Create your models here.
class Patient(models.Model):
    patient_id = models.AutoField(primary_key=True, default=0)
    name = models.CharField(max_length=10)
    email_id = models.CharField(max_length=10)
    birth_date = models.CharField(max_length=12)
    adhaar_number = models.CharField(max_length=12)
    permission = models.CharField(max_length=3)
    gender = models.CharField(max_length=10)
    age = models.CharField(max_length=3)
    address_1 = models.CharField(max_length=10)
    city = models.CharField(max_length=10)
    state = models.CharField(max_length=10)
    country = models.CharField(max_length=10)
    pincode = models.CharField(max_length=6)
    def __str__(self):
        return self.patient_id

# class phone_number(models.Model):
#     phone_number_id = models.CharField(max_length=10, primary_key=True)
#     patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
#     phone_number = models.CharField(max_length=10)
#     def __str__(self):
#         return str(self.phone_number_id)

# class file(models.Model):
#     file_id = models.CharField(max_length=10, primary_key=True)
#     patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
#     doctor_id = models.CharField(max_length=10)
#     symptoms = models.CharField(max_length=10)
#     diagnosis = models.CharField(max_length=10)
#     prescribed_medicine = models.CharField(max_length=10)
#     notes = models.CharField(max_length=10)
#     created_date = models.CharField(max_length=10)
#     def __str__(self):
#         return str(self.file_id)

# class health_info(models.Model):
#     health_id = models.CharField(max_length=10, primary_key=True)
#     patient_id = models.CharField(max_length=10)
#     height = models.CharField(max_length=10)
#     weight = models.CharField(max_length=10)
#     blood_grp = models.CharField(max_length=10)
#     emergency_num = models.CharField(max_length=10)
#     medication = models.CharField(max_length=10)
#     def __str__(self):
#         return str(self.health_id)
