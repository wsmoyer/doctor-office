from django import forms
from bootstrap_datepicker_plus import DatePickerInput
from .models import Patient
from .models import Appointment,PrescriptionRefillRequest
from django.core.mail import send_mail

class MakeAppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        exclude = ('patient','email')
    appointment_date = forms.DateField(widget=DatePickerInput())
  
    
        
class RefillForm(forms.ModelForm):
    class Meta:
        model = PrescriptionRefillRequest
        exclude = ('requested_by',)        


class DoctorContactForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea)
    email = forms.CharField()
    doctor_email = forms.CharField()

    def send_email(self):

        send_mail('Doctor Appointment Confirmation',self.cleaned_data['message'],self.cleaned_data['email'],[self.cleaned_data['doctor_email']],fail_silently=False)
