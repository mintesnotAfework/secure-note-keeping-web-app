from django.shortcuts import render
from django.http import HttpResponseRedirect,Http404,HttpResponseServerError,HttpResponseBadRequest
from django.urls import reverse
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.models import User
from authentication.validation import validate_password
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from authentication.models import UserProfile


class Index(LoginRequiredMixin,View):
    login_url = "/login"
    def get(self, requests):
        return HttpResponseRedirect(reverse("note:index"))


class LoginView(View):
    def get(self,requests):
        return render(requests,"authentication/login/index.html")
    
    def post(self,requests):
        username = requests.POST["username"]
        password = requests.POST["password"]
        user = authenticate(requests, username=username, password=password)
        if user is not None:
            login(requests,user)
            return HttpResponseRedirect(reverse("note:index",))
        else:
            message = "Invalid username or password"
        return render(requests,"authentication/login/index.html",{"message" : message})


class RegistrationView(View):
    def get(self,requests):
        return render(requests,"authentication/login/index.html")

    def post(self,requests):
        message=""
        if not (validate_password(requests.POST.get("password1"))):
            message = "The password is invalid\nMake sure it has captial and small letter with number and special character"
        elif requests.POST.get("password1") == requests.POST.get("password2"):
            message = "The password are not the same"
        elif requests.POST.get["email"] == "":
            message = "Email field can not be empty"
        elif requests.POST.get["firstname"] == "":
            message = "First name can not be empty"
        elif requests.POST.get["lastname"] == "":
            message = "Last name can not be empty"
        else:
            try:
                user_temp = User.objects.get(username=requests.POST.get("username"))
            except:
                user = User.objects.create_user(requests.POST.get("username"), requests.POST.get("email"), requests.POST.get("password1"))
                user.first_name = requests.POST.get("firstname")
                user.last_name = requests.POST.get("lastname")
                user.save()
            else:
                message = "Username is taken"
        return render(requests,"authentication/login/index.html",{"message":message,})

class LogoutView(LoginRequiredMixin,View):
    login_url="/login/"
    def get(self,requests):
        logout(requests)
        return HttpResponseRedirect(reverse("authentication:index",))
    
class PasswordRestView(LoginRequiredMixin,View):
    login_url = "/login/"
    def get(self,requests):
        return render(requests,"authentication/reset/index.html")
    
    def post(self,requests):
        message = ""
        if not (validate_password(requests.POST.get("password1"))):
            message = "The password is invalid\nMake sure it has captial and small letter with number and special character"
        elif requests.POST.get("password1") == requests.POST.get("password2") and requests.POST.get("password1") != "":
            user = requests.user
            user.set_password(requests.POST.get("password1"))
            user.save()
            return HttpResponseRedirect(reverse("note:index",))
        elif requests.POST.get("password1") == requests.POST.get("password2"):
            message = "The password field is not the same"
        elif requests.POST.get("password1") == "":
            message = "The password field is required"
        return render(requests,"authentication/reset/index.html",{"message":message,})


class UpdateView(LoginRequiredMixin,View):
    login_url = "/login/"
    def get(self,requests):
        user = User.objects.get(id = requests.user.id)
        return render(requests,"authentication/reset/index.html",{"user":user})

    def post(self,requests):
        user = User.objects.get(id = requests.user.id)
        try:
            user.first_name = requests.POST.get("firstname")
            user.last_name = requests.POST.get("lastname")
            user.email = requests.POST.get("email")
            user.save()
            return HttpResponseRedirect(reverse("note:index",))
        except:
            return render(requests,"authentication/reset/index.html",{"user":user})


class ForgetView(View):
    def get(self,requests):
        pass

    def post(self,requests):
        pass