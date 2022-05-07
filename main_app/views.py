from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from  .forms import *

from django.contrib import messages
from .decorators import *
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@unautheticated_user
def loginPage(request):
    
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(request,username=username,password=password)
        if user != None:
            login(request, user)
            user_type = user.user_type
            if user_type == '1':
                return redirect('/')
            elif user_type == '2':
                return redirect('dash')
            elif user_type == '3':
                return redirect('customer')
            else:
                messages.error(request, "Invalid Login!")
                return redirect('login')
        else:
            messages.error(request, "Invalid Login Credentials!")
            return redirect('login')
    
    return render(request,'auth/login.html')



def logoutUser(request):
    logout(request)
    return redirect('login')







def customer_signup_view(request):
    form=PatientForm()
    context={
        'form':form
    }
    if request.method=='POST':
        form=PatientForm(request.POST)
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        if  form.is_valid():
            user = CustomUser.objects.create_user(username=username, email=email,password=password, first_name=first_name, last_name=last_name,user_type=3 )
            user.customer.address = address
            user.customer.mobile = mobile
            user.save()
            messages.success(request, "Account Created Succefully")

        return redirect('login')

    context={
    "title":"Add Vet",
    'form':form
    }
     
    
    return render(request,'auth/customerSignUp.html',context)
# Email ,username validation

@csrf_exempt
def check_email_exist(request):
    email = request.POST.get("email")
    user_obj = CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@csrf_exempt
def check_username_exist(request):
    username = request.POST.get("username")
    user_obj = CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

