from celery import shared_task

from .models import Appointment,Patient
from django.core.mail import send_mail
from datetime import date


@shared_task
def remind_patient():
    need_reminders = Appointment.objects.filter(appointment_date__date=date.today())
    print(need_reminders)
    for patient in need_reminders:
        send_mail('Doctor Appointment Confirmation','Your Appointment has been scheduled for','wsmoyer313@gmail.com',[patient.email],fail_silently=False)
