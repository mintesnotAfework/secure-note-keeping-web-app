from django.shortcuts import render
from django.http import HttpResponsePermanentRedirect
from .forms import LoginForm,RegistrationForm,UpdateForm,PasswordResetForm
from django.urls import reverse
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.models import User
from authentication.validation import validate_password
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from authentication.models import UserProfile
from note import cryptoengine
import random


class Index(LoginRequiredMixin,View):
    login_url = "/login"
    def get(self, requests):
        return HttpResponsePermanentRedirect(reverse("note:index"))


class LoginView(View):
    def get(self,requests):
        return render(requests,"authentication/login/index.html")
    
    def post(self,requests):
        login_form = LoginForm(data=requests.POST)
        if login_form.is_valid():
            username = requests.POST["username"]
            password = requests.POST["password"]
            user = authenticate(requests, username=username, password=password)
            if user is not None:
                login(requests,user)
                return HttpResponsePermanentRedirect(reverse("note:index",))
        message = "Invalid username or password"
        return render(requests,"authentication/login/index.html",{"message" : message})


class RegistrationView(View):
    def get(self,requests):
        return render(requests,"authentication/login/index.html")

    def post(self,requests):
        registeration_form = RegistrationForm(data=requests.POST)
        if registeration_form.is_valid():
            message=""
            if not (validate_password(requests.POST.get("password1"))):
                message = "The password is invalid\nMake sure it has captial and small letter with number and special character"
            elif not requests.POST.get("password1") == requests.POST.get("password2"):
                message = "The password does not match"
            else:
                try:
                    user_temp = User.objects.get(username=requests.POST.get("username"))
                except:
                    user = User.objects.create_user(requests.POST.get("username"), requests.POST.get("email"), requests.POST.get("password1"))
                    user.first_name = requests.POST.get("firstname")
                    user.last_name = requests.POST.get("lastname")
                    user.save()
                    file_path = cryptoengine.MessageDigest.sha256_hash(user.username + str(random.randbytes))
                    while len(UserProfile.objects.filter(file_path = file_path)) != 0:
                        file_path = cryptoengine.MessageDigest.sha256_hash(user.username + str(random.randbytes))
                    cryptoengine.RSACryptography.key_generation(file_path)
                    aes_secret_key = cryptoengine.AESCryptography.key_generation(requests.POST.get("password1"))
                    singed_aes_key = cryptoengine.RSACryptography.sign(aes_secret_key)
                    aes_rsa_encrytion = cryptoengine.RSACryptography.encryption(file_path,aes_secret_key)
                    user_profile = UserProfile(user_user=user,signed_password=singed_aes_key, hashed_password=aes_rsa_encrytion,file_path=file_path)
                    user_profile.save()
                else:
                    message = "Username is taken"
        else:
            message = registeration_form.errors
        return render(requests,"authentication/login/index.html",{"message":message,})

class LogoutView(LoginRequiredMixin,View):
    login_url="/login/"
    def get(self,requests):
        logout(requests)
        return HttpResponsePermanentRedirect(reverse("authentication:index",))
    
class PasswordRestView(LoginRequiredMixin,View):
    login_url = "/login/"
    def get(self,requests):
        user = User.objects.get(id = requests.user.id)
        user_profile = UserProfile.objects.get(user_user = user)
        return render(requests,"authentication/reset/index.html",{"user":user,"user_profile":user_profile})
    
    def post(self,requests):
        password_reset_form = PasswordResetForm(data=requests.POST)
        if password_reset_form.is_valid():
            message = ""
            if not (validate_password(requests.POST.get("password1"))):
                message = "The password is invalid\nMake sure it has captial and small letter with number and special character"
            elif requests.POST.get("password1") == requests.POST.get("password2"):
                user = requests.user
                user.set_password(requests.POST.get("password1"))
                user.save()
                return HttpResponsePermanentRedirect(reverse("note:index",))
            elif requests.POST.get("password1") != requests.POST.get("password2"):
                message = "The password field is not the same"
            elif requests.POST.get("password1") == "":
                message = "The password field is required"
        else:
            message = password_reset_form.errors
        user = User.objects.get(id = requests.user.id)
        user_profile = UserProfile.objects.get(user_user = user)
        return render(requests,"authentication/reset/index.html",{"message":message,"user":user,"user_profile":user_profile})


class UpdateView(LoginRequiredMixin,View):
    login_url = "/login/"
    def get(self,requests):
        user = User.objects.get(id = requests.user.id)
        user_profile = UserProfile.objects.get(user_user = user)
        return render(requests,"authentication/reset/index.html",{"user":user,"user_profile":user_profile})

    def post(self,requests):
        user = User.objects.get(id = requests.user.id)
        user_profile = UserProfile.objects.get(user_user = user)
        update_form = UpdateForm(data=requests.POST)
        if update_form.is_valid():
            user.first_name = requests.POST.get("firstname")
            user.last_name = requests.POST.get("lastname")
            user.email = requests.POST.get("email")
            user_profile.profile_picture = requests.FILES['profile_picture']
            user.save()
            user_profile.save()
            return HttpResponsePermanentRedirect(reverse("note:index",))
        else:
            return render(requests,"authentication/reset/index.html",{"user":user,"user_profile":user_profile,"form":update_form.errors})


class ForgetView(View):
    def get(self,requests):
        return render(requests,"authentication/forget/index.html")

    def post(self,requests):
        return HttpResponsePermanentRedirect(reverse("authentication:index",))
    

class AboutView(View):
    def get(self,requests):
        return render(requests,"bio/index.html")