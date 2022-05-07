from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import admin
import datetime
from django.core.cache import cache
from django.conf import settings


#Check whether the user is logged in or not

class LoginCheckMiddleWare(MiddlewareMixin):
   
    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__
        user = request.user
        if user.is_authenticated:
            if user.user_type == "1":
                
                if modulename == "main_app.agrovet_views.adminView": 
                    pass
               
                elif modulename == "main_app.views" or modulename == "django.views.static":
                    pass
                else:
                    return redirect("/")
  
            elif user.user_type == "2":
         
                if modulename == "main_app.agrovet_views.vetViews":
                    pass
                elif modulename == "main_app.views" or modulename == "django.views.static":
                    pass
                else:
                    return redirect("dash")
            elif user.user_type == "3":
             
                if modulename == "main_app.agrovet_views.customerViews":
                    pass
                elif modulename == "main_app.views" or modulename == "django.views.static":
                    pass
                else:
                    return redirect("customer")
          
          
        else:
            if request.path == reverse("login"):
                pass
            elif request.path == reverse("signup"):
                pass
            else:
                return redirect("login")


     #NB: Email confirmation will not occur       
    #  or request.path == reverse("reset_password") or request.path == reverse("password_reset_done") or request.path == reverse("password_reset_complete")