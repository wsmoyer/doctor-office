from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from datetime import datetime,timedelta,date
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


# Create your models here.

class Provider(models.Model):
    name = models.CharField(max_length=50)


    def __str__(self):
        return self.name




class Doctor(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return self.first_name + " " + self.last_name



class Patient(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    doctor = models.ForeignKey(Doctor,on_delete=models.DO_NOTHING,blank=True,null=True)
    email = models.EmailField()
    insurance_provider = models.ForeignKey(Provider,on_delete=models.DO_NOTHING,blank=True,null=True)
    preferred_pharmacy = models.CharField(max_length=100,null=True)
def get_deadline():
    return date.today() + timedelta(days=7)


def validate_date(value):
    if value  <= get_deadline():
        raise ValidationError(
            'Appointment needs to be scheduled at least 7 days in advance'
            #params={'value': value},
        )


class Appointment(models.Model):
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE)
    reason_for_visit = models.TextField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date = models.DateField(auto_now_add=True)
    appointment_date = models.DateField(default=get_deadline,validators=[validate_date])
    email = models.EmailField()



    def __str__(self):
        return self.last_name + ", " + self.first_name
    

class Medication(models.Model):
    name = models.CharField(max_length=50)
    perscribed_to = models.ForeignKey(Patient,on_delete=models.DO_NOTHING)
    perscribed_by = models.ForeignKey(Doctor,on_delete=models.DO_NOTHING)
    instructions = models.TextField()
    
    def __str__(self):
        return self.name


class PrescriptionRefillRequest(models.Model):
    medication = models.ForeignKey(Medication,on_delete=models.CASCADE)
    requested_by = models.ForeignKey(Patient,on_delete=models.CASCADE)
    date_requested = models.DateField(auto_now_add=True)
    pharmacy_location = models.CharField(max_length=100)


    def __str__(self):
        return self.medication


