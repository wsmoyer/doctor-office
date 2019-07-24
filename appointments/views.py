from django.shortcuts import render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView,DetailView,CreateView
from django.views.generic.edit import UpdateView,FormView
from .models import Appointment,Patient,Medication,PrescriptionRefillRequest
from .forms import MakeAppointmentForm,RefillForm,DoctorContactForm
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.contrib import messages
from datetime import datetime,timedelta
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
class Index(LoginRequiredMixin,TemplateView):
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['medications'] = Medication.objects.filter(perscribed_to=self.request.user.id)

        try:
            context['appointment'] =  Appointment.objects.get(patient=self.request.user.id)
            return context
        except ObjectDoesNotExist:
            pass
        return context
    

            
class MakeAppointment(LoginRequiredMixin,CreateView):
    model = Appointment
    template_name = 'appointment_form.html'
    
    form_class = MakeAppointmentForm
    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.patient = self.request.user
        self.object.email = Patient.objects.only('email').get(pk=self.request.user.id).email
        print(self.object.email)
        try:
            user = Appointment.objects.get(patient=self.request.user)
        except Appointment.DoesNotExist:
            user = None
        if user is not None:
            error =  messages.error(self.request,"You have already scheduled an appointment.")
            return redirect('/')
        
            
        else:
            # email = self.object.email            
            # send_mail('Doctor Appointment Confirmation',f'Your Appointment has been scheduled for {self.object.appointment_date}','wsmoyer313@gmail.com',[email],fail_silently=False)
            # messages.success(self.request,"Your appointment has been scheduled")

            self.object.save()
            return redirect('/')


class ViewAppointment(LoginRequiredMixin,DetailView):
    model = Appointment
    template_name = 'appointment_detail.html'

    def get_queryset(self):
        return Appointment.objects.filter(patient=self.request.user.id)
        

class UpdatePatient(LoginRequiredMixin,UpdateView):
    model = Patient
    fields = ('first_name','last_name','doctor','email','insurance_provider','preferred_pharmacy','phone_number')
    def form_valid(self,form):

        messages.success(self.request,"Your profile has been updated.")
        form.save()
        return redirect('/')
    template_name = 'patient_update.html'


class RefillRequest(LoginRequiredMixin,CreateView):
    model = PrescriptionRefillRequest
    template_name = 'refill_request.html'
    form_class = RefillForm
    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.requested_by = self.request.user
        messages.success(self.request,"Refill request has been submitted.")

        self.object.save()
        return redirect('/')



class DoctorContactForm(LoginRequiredMixin,FormView):
    template_name = 'contact_doctor.html'
    form_class = DoctorContactForm
    success_url = '/'
    def form_valid(self,form):
        form.send_email()
        messages.success(self.request,"Your have successfully sent an email to your doctor.")
        return super().form_valid(form)
