from django import forms
from bootstrap_datepicker_plus import DatePickerInput
from .models import Patient
from .models import Appointment,PrescriptionRefillRequest,Prescription
from django.core.mail import send_mail
from django.contrib.auth.forms import UserCreationForm
from .models import Patient
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


class DoctorPerscriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        exclude = ('perscribed_by',)     


class UserRegister(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Patient
        fields = UserCreationForm.Meta.fields + ('email','phone_number','first_name','last_name','insurance_provider')
