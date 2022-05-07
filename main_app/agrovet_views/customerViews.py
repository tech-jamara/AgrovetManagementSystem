from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from main_app.forms import *
from main_app.models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from datetime import datetime
from django.db.models import Sum
from django.views.generic import (View)
from django.core.files.storage import FileSystemStorage 


def customer_dashboard(request):

    return render(request, 'customer/dashboard.html')

def profile(request):
    customuser=CustomUser.objects.get(id=request.user.id)
    admin=Customer.objects.get(admin=customuser.id)
    context={
        "admin":admin,
    }

    return render(request,'customer/customerProfile/profile.html',context)


def edit_profile(request):
    customuser=CustomUser.objects.get(id=request.user.id)
    admin=Customer.objects.get(admin=customuser.id)

    form=PatientForm()
    if request.method == 'POST':
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        email=request.POST.get('email')
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')


        customuser=CustomUser.objects.get(id=request.user.id)
        customuser.first_name=first_name
        customuser.last_name=last_name
        customuser.email = email
        customuser.password=password
        customuser.save()

        admin=Customer.objects.get(admin=customuser.id)
        form =PatientForm(request.POST,request.FILES,instance=admin)
        admin.address = address
        admin.mobile=mobile
        admin.save()

        if form.is_valid():
            form.save()

    context={
        "form":form,
        "admin":admin,
        "user":customuser
    }

    return render(request,'customer/customerProfile/edit_profile.html',context)


def make_appointment(request):
    form=AppointmentForm()
    context={'form':form}
    if request.method=='POST':
        form=AppointmentForm(request.POST)
     
        if form.is_valid():
            form=AppointmentForm(request.POST,request.FILES)
            if len(request.FILES) != 0:
                profile_pic = request.FILES['pic']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None
            appointment=form.save(commit=False)
            appointment.customerId=request.user.id 
            appointment.customerName=request.user 
            appointment.pic = profile_pic_url
            appointment.status=False
            appointment.save()
            messages.success(request, "Appointment sent successfully")

            return redirect('appoint-make')
      

    context={
        'form':form
    }
    return render(request,'customer/appointment/make.html',context)
    


def manage_appointment(request):
    appnt = Appointment.objects.all()
    context={
        'appnt':appnt
    }
    return render(request,'customer/appointment/view.html',context)



