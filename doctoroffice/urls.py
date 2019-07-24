"""doctoroffice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from appointments.views import Index,MakeAppointment,ViewAppointment,UpdatePatient,RefillRequest,DoctorContactForm
from med_blog.views import PostList


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login',auth_views.LoginView.as_view(template_name='login.html'),name='login'),
    path('logout',auth_views.LogoutView.as_view(template_name='index.html'),name='logout'),
    path('',Index.as_view(),name='home'),
    path('appointments/make',MakeAppointment.as_view(),name="make-appointment"),
    path('blog/', include('med_blog.urls')),
    path('appointment/<int:pk>',ViewAppointment.as_view(),name='appointment-detail'),
    path('patient/<int:pk>',UpdatePatient.as_view(),name='patient-update'),
    path('request-refill',RefillRequest.as_view(),name='refill-request'),
    path('contact-doctor',DoctorContactForm.as_view())
    ]
