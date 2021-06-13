from django.contrib import admin

from .models import * 
# Register your models here.
admin.site.register(Patient)
admin.site.register(PhoneNumber)
admin.site.register(Doctor)
admin.site.register(File)
admin.site.register(HealthInfo)
admin.site.register(Allergies)
admin.site.register(Metadata)
admin.site.register(Admin)
admin.site.register(VerifiedBy)
admin.site.register(Paramedics)

