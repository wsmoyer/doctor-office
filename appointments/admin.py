from django.contrib import admin
from .models import Appointment
# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import Patient,Doctor,Medication,PrescriptionRefillRequest,Provider,Prescription

admin.site.register(Patient, UserAdmin)
admin.site.register(Appointment)
admin.site.register(Doctor)
admin.site.register(Medication)
admin.site.register(PrescriptionRefillRequest)
admin.site.register(Provider)
admin.site.register(Prescription)