from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from datetime import datetime,timedelta,date
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator


# Create your models here.

class Provider(models.Model):
    name = models.CharField(max_length=50)


    def __str__(self):
        return self.name


class RegisteredPharmacyLocations(models.Model):
    name = models.CharField(max_length=75)


    def __str__(self):
        return self.name 



class Doctor(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True) # validators should be a list
    def __str__(self):
        return self.first_name + " " + self.last_name



class Patient(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    doctor = models.ForeignKey(Doctor,on_delete=models.DO_NOTHING,blank=True,null=True)
    email = models.EmailField()
    insurance_provider = models.ForeignKey(Provider,on_delete=models.DO_NOTHING,blank=True,null=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True) # validators should be a list
    preferred_pharmacy = models.ForeignKey(RegisteredPharmacyLocations,on_delete=models.DO_NOTHING,null=True)

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
    price = models.DecimalField(max_digits=6,decimal_places=2,blank=True,null=True)
    def __str__(self):
        return self.name



class PrescriptionRefillRequest(models.Model):
    medication = models.ForeignKey(Medication,on_delete=models.CASCADE,null=True)
    requested_by = models.ForeignKey(Patient,on_delete=models.CASCADE,null=True)
    date_requested = models.DateField(auto_now_add=True)


    def __str__(self):
        return self.medication

